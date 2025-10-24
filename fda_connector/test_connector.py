"""
Test script for FDA Connector

Run this locally to test the connector before deploying to Fivetran
"""

import json
from connector import FDAConnector

def test_connector():
    """Test the FDA connector locally"""
    
    # Test configuration
    config = {
        "endpoint": "drug_adverse_events",
        "start_date": "2024-01-01",
        "limit_per_request": 10
    }
    
    print("=" * 60)
    print("FDA Connector Test")
    print("=" * 60)
    print(f"Configuration: {json.dumps(config, indent=2)}")
    print()
    
    # Initialize connector
    connector = FDAConnector(config)
    
    # Test schema
    print("Schema:")
    print(json.dumps(connector.schema(), indent=2))
    print()
    
    # Test sync
    print("Testing sync (first 10 records)...")
    state = {}
    record_count = 0
    
    for message in connector.update(state):
        if message["type"] == "UPSERT":
            record_count += 1
            print(f"\nRecord {record_count}:")
            print(json.dumps(message["data"], indent=2))
            
            if record_count >= 3:  # Only show first 3 for testing
                print("\n... (showing first 3 records only)")
                break
                
        elif message["type"] == "STATE":
            print(f"\nState update: {message['data']}")
    
    print(f"\nTest completed. Fetched {record_count} records.")
    print("=" * 60)


if __name__ == "__main__":
    test_connector()


