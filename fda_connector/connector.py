"""
FDA Data Connector for Fivetran Connector SDK

This connector fetches data from the FDA's openFDA API and makes it available
for ingestion into Google Cloud destinations (BigQuery, Cloud Storage, Cloud SQL).

Supported endpoints:
- Drug adverse events
- Drug labeling
- Device adverse events
- Food recalls
"""

import requests
from datetime import datetime, timedelta
import time
from typing import Dict, Any, Generator, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FDAConnector:
    """
    FDA Data Connector for Fivetran
    
    Fetches data from openFDA API endpoints and yields records
    in Fivetran-compatible format.
    """
    
    BASE_URL = "https://api.fda.gov"
    
    # Available endpoints
    ENDPOINTS = {
        "drug_adverse_events": "/drug/event.json",
        "drug_labels": "/drug/label.json",
        "device_adverse_events": "/device/event.json",
        "food_recalls": "/food/enforcement.json",
        "drug_recalls": "/drug/enforcement.json"
    }
    
    def __init__(self, configuration: Dict[str, Any]):
        """
        Initialize the connector with configuration
        
        Args:
            configuration: Dict containing:
                - api_key: FDA API key (optional but recommended)
                - endpoint: Which FDA endpoint to sync
                - start_date: Start date for data fetch (YYYY-MM-DD)
                - limit_per_request: Records per API request (max 1000)
        """
        self.api_key = configuration.get("api_key")
        self.endpoint = configuration.get("endpoint", "drug_adverse_events")
        self.start_date = configuration.get("start_date")
        self.limit_per_request = min(int(configuration.get("limit_per_request", 100)), 1000)
        
        if self.endpoint not in self.ENDPOINTS:
            raise ValueError(f"Invalid endpoint. Choose from: {list(self.ENDPOINTS.keys())}")
    
    def _make_request(self, url: str, params: Dict[str, Any]) -> Optional[Dict]:
        """
        Make API request with error handling and rate limiting
        
        Args:
            url: Full API URL
            params: Query parameters
            
        Returns:
            JSON response or None if error
        """
        if self.api_key:
            params["api_key"] = self.api_key
        
        try:
            response = requests.get(url, params=params, timeout=30)
            
            # Handle rate limiting
            if response.status_code == 429:
                logger.warning("Rate limit hit, waiting 60 seconds...")
                time.sleep(60)
                return self._make_request(url, params)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
    
    def _build_search_query(self, skip: int) -> str:
        """
        Build search query based on endpoint and state
        
        Args:
            skip: Number of records to skip
            
        Returns:
            Query string for FDA API
        """
        params = {
            "limit": self.limit_per_request,
            "skip": skip
        }
        
        # Add date filter if start_date provided
        if self.start_date:
            if self.endpoint in ["drug_adverse_events", "device_adverse_events"]:
                params["search"] = f"receivedate:[{self.start_date.replace('-', '')} TO 99991231]"
            elif "recalls" in self.endpoint or "enforcement" in self.endpoint:
                params["search"] = f"report_date:[{self.start_date.replace('-', '')} TO 99991231]"
        
        return params
    
    def schema(self) -> Dict[str, Any]:
        """
        Define the schema for Fivetran
        
        Returns:
            Schema definition with tables and columns
        """
        # Base schema varies by endpoint
        if self.endpoint == "drug_adverse_events":
            return {
                "table": "fda_drug_adverse_events",
                "primary_key": ["safetyreportid"],
                "columns": {
                    "safetyreportid": "STRING",
                    "receivedate": "STRING",
                    "patient_age": "FLOAT",
                    "patient_sex": "STRING",
                    "serious": "STRING",
                    "serious_death": "STRING",
                    "serious_hospitalization": "STRING",
                    "drug_names": "STRING",  # JSON array as string
                    "reactions": "STRING",  # JSON array as string
                    "fetched_at": "TIMESTAMP"
                }
            }
        elif self.endpoint == "drug_labels":
            return {
                "table": "fda_drug_labels",
                "primary_key": ["id"],
                "columns": {
                    "id": "STRING",
                    "effective_time": "STRING",
                    "product_name": "STRING",
                    "generic_name": "STRING",
                    "manufacturer": "STRING",
                    "indications_and_usage": "STRING",
                    "warnings": "STRING",
                    "dosage_and_administration": "STRING",
                    "fetched_at": "TIMESTAMP"
                }
            }
        elif self.endpoint == "food_recalls":
            return {
                "table": "fda_food_recalls",
                "primary_key": ["recall_number"],
                "columns": {
                    "recall_number": "STRING",
                    "report_date": "STRING",
                    "product_description": "STRING",
                    "reason_for_recall": "STRING",
                    "company_name": "STRING",
                    "classification": "STRING",
                    "status": "STRING",
                    "distribution_pattern": "STRING",
                    "fetched_at": "TIMESTAMP"
                }
            }
        elif self.endpoint == "drug_recalls":
            return {
                "table": "fda_drug_recalls",
                "primary_key": ["recall_number"],
                "columns": {
                    "recall_number": "STRING",
                    "report_date": "STRING",
                    "product_description": "STRING",
                    "reason_for_recall": "STRING",
                    "company_name": "STRING",
                    "classification": "STRING",
                    "status": "STRING",
                    "fetched_at": "TIMESTAMP"
                }
            }
        else:  # device_adverse_events
            return {
                "table": "fda_device_adverse_events",
                "primary_key": ["mdr_report_key"],
                "columns": {
                    "mdr_report_key": "STRING",
                    "report_number": "STRING",
                    "date_received": "STRING",
                    "device_name": "STRING",
                    "manufacturer": "STRING",
                    "event_type": "STRING",
                    "adverse_event_flag": "STRING",
                    "patient_problem": "STRING",
                    "fetched_at": "TIMESTAMP"
                }
            }
    
    def _extract_record_data(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract and normalize record data based on endpoint
        
        Args:
            result: Raw API result
            
        Returns:
            Normalized record
        """
        fetched_at = datetime.utcnow().isoformat()
        
        if self.endpoint == "drug_adverse_events":
            patient = result.get("patient", {})
            reactions = [r.get("reactionmeddrapt", "") for r in patient.get("reaction", [])]
            drugs = [d.get("medicinalproduct", "") for d in patient.get("drug", [])]
            
            return {
                "safetyreportid": result.get("safetyreportid", ""),
                "receivedate": result.get("receivedate", ""),
                "patient_age": patient.get("patientonsetage", 0.0) if patient.get("patientonsetage") else None,
                "patient_sex": patient.get("patientsex", ""),
                "serious": str(result.get("serious", "")),
                "serious_death": str(result.get("seriousnessdeath", "")),
                "serious_hospitalization": str(result.get("seriousnesshospitalization", "")),
                "drug_names": str(drugs),
                "reactions": str(reactions),
                "fetched_at": fetched_at
            }
            
        elif self.endpoint == "drug_labels":
            openfda = result.get("openfda", {})
            return {
                "id": result.get("id", ""),
                "effective_time": result.get("effective_time", ""),
                "product_name": ", ".join(openfda.get("brand_name", [])),
                "generic_name": ", ".join(openfda.get("generic_name", [])),
                "manufacturer": ", ".join(openfda.get("manufacturer_name", [])),
                "indications_and_usage": " ".join(result.get("indications_and_usage", [])),
                "warnings": " ".join(result.get("warnings", [])),
                "dosage_and_administration": " ".join(result.get("dosage_and_administration", [])),
                "fetched_at": fetched_at
            }
            
        elif self.endpoint in ["food_recalls", "drug_recalls"]:
            return {
                "recall_number": result.get("recall_number", ""),
                "report_date": result.get("report_date", ""),
                "product_description": result.get("product_description", ""),
                "reason_for_recall": result.get("reason_for_recall", ""),
                "company_name": result.get("recalling_firm", ""),
                "classification": result.get("classification", ""),
                "status": result.get("status", ""),
                "distribution_pattern": result.get("distribution_pattern", "") if self.endpoint == "food_recalls" else "",
                "fetched_at": fetched_at
            }
            
        else:  # device_adverse_events
            return {
                "mdr_report_key": result.get("mdr_report_key", ""),
                "report_number": result.get("report_number", ""),
                "date_received": result.get("date_received", ""),
                "device_name": result.get("device", [{}])[0].get("generic_name", "") if result.get("device") else "",
                "manufacturer": result.get("device", [{}])[0].get("manufacturer_d_name", "") if result.get("device") else "",
                "event_type": result.get("event_type", ""),
                "adverse_event_flag": result.get("adverse_event_flag", ""),
                "patient_problem": ", ".join([p.get("patient_problem_code", "") for p in result.get("patient", [])]) if result.get("patient") else "",
                "fetched_at": fetched_at
            }
    
    def update(self, state: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
        """
        Main sync method that yields records
        
        Args:
            state: Previous state from Fivetran
            
        Yields:
            Records and state updates
        """
        skip = state.get("skip", 0)
        total_synced = 0
        
        endpoint_url = f"{self.BASE_URL}{self.ENDPOINTS[self.endpoint]}"
        
        logger.info(f"Starting sync for {self.endpoint} from skip={skip}")
        
        while True:
            params = self._build_search_query(skip)
            
            logger.info(f"Fetching records at skip={skip}")
            response_data = self._make_request(endpoint_url, params)
            
            if not response_data or "results" not in response_data:
                logger.warning("No more results or error occurred")
                break
            
            results = response_data.get("results", [])
            
            if not results:
                logger.info("No more results available")
                break
            
            # Process and yield records
            for result in results:
                try:
                    record = self._extract_record_data(result)
                    
                    # Yield the record
                    yield {
                        "type": "UPSERT",
                        "table": self.schema()["table"],
                        "data": record
                    }
                    
                    total_synced += 1
                    
                except Exception as e:
                    logger.error(f"Error processing record: {e}")
                    continue
            
            # Update skip position
            skip += len(results)
            
            # Yield state checkpoint
            yield {
                "type": "STATE",
                "data": {"skip": skip}
            }
            
            # Check if we got fewer results than requested (end of data)
            if len(results) < self.limit_per_request:
                logger.info(f"Reached end of data. Total synced: {total_synced}")
                break
            
            # Rate limiting - be nice to FDA API
            time.sleep(0.5)
        
        logger.info(f"Sync complete. Total records synced: {total_synced}")


# Fivetran SDK entry points
def schema(configuration: Dict[str, Any]) -> Dict[str, Any]:
    """Schema definition entry point"""
    connector = FDAConnector(configuration)
    return connector.schema()


def update(configuration: Dict[str, Any], state: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
    """Sync entry point"""
    connector = FDAConnector(configuration)
    yield from connector.update(state)


