# FDA Data Connector for Fivetran

A custom Fivetran connector that syncs data from the FDA's openFDA API to Google Cloud destinations (BigQuery, Cloud Storage, Cloud SQL).

## Features

- ✅ Syncs multiple FDA datasets:
  - Drug adverse events
  - Drug labels
  - Device adverse events
  - Food recalls
  - Drug recalls
- ✅ Incremental syncing with state management
- ✅ Rate limiting and error handling
- ✅ Configurable date ranges
- ✅ Production-ready for Fivetran deployment

## Prerequisites

1. **Fivetran Account**: [Sign up for a 14-day free trial](https://fivetran.com/signup)
2. **Google Cloud Account**: Set up with BigQuery enabled
3. **FDA API Key** (optional but recommended): [Get one here](https://open.fda.gov/apis/authentication/)

## Local Testing

### Setup
```bash
cd fda_connector
pip install -r requirements.txt
```

### Test the Connector
```bash
python test_connector.py
```

## Deployment to Fivetran

### Method 1: Using Fivetran CLI

1. **Install Fivetran CLI**:
```bash
pip install fivetran-connector-sdk
```

2. **Deploy the Connector**:
```bash
fivetran-connector deploy \
  --name "FDA Data Connector" \
  --description "Syncs FDA data to Google Cloud" \
  --connector-file connector.py \
  --config-file configuration.json \
  --requirements requirements.txt
```

3. **Configure in Fivetran Dashboard**:
   - Navigate to Fivetran dashboard
   - Add new connector → Custom Connector
   - Select your deployed FDA connector
   - Configure settings:
     - FDA Endpoint (choose from dropdown)
     - Start Date (optional)
     - API Key (optional)
   - Select your Google Cloud destination

### Method 2: Manual Upload

1. Package the connector:
```bash
zip -r fda_connector.zip connector.py configuration.json requirements.txt
```

2. Upload to Fivetran:
   - Go to Fivetran dashboard
   - Navigate to Connectors → Custom Connectors
   - Upload the zip file
   - Follow the configuration wizard

## Configuration Options

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `endpoint` | FDA dataset to sync | Yes | `drug_adverse_events` |
| `api_key` | FDA API key | No | None |
| `start_date` | Start date (YYYY-MM-DD) | No | All data |
| `limit_per_request` | Records per request (max 1000) | No | 100 |

### Available Endpoints

1. **drug_adverse_events**: Reports of adverse events for drugs
2. **drug_labels**: Drug labeling information
3. **device_adverse_events**: Medical device adverse events
4. **food_recalls**: Food product recalls
5. **drug_recalls**: Drug product recalls

## Data Schema

### Drug Adverse Events
- `safetyreportid` (PRIMARY KEY)
- `receivedate`
- `patient_age`
- `patient_sex`
- `serious`
- `drug_names`
- `reactions`
- `fetched_at`

### Drug Labels
- `id` (PRIMARY KEY)
- `product_name`
- `generic_name`
- `manufacturer`
- `indications_and_usage`
- `warnings`
- `dosage_and_administration`
- `fetched_at`

### Food/Drug Recalls
- `recall_number` (PRIMARY KEY)
- `report_date`
- `product_description`
- `reason_for_recall`
- `company_name`
- `classification`
- `status`
- `fetched_at`

## Rate Limits

- **Without API Key**: 240 requests/minute, 1,000 requests/day
- **With API Key**: 240 requests/minute, 120,000 requests/day

## Troubleshooting

### Issue: Rate limit errors
**Solution**: Add an FDA API key or reduce `limit_per_request`

### Issue: No data syncing
**Solution**: Check start_date format (YYYY-MM-DD) and ensure it's not too recent

### Issue: Connection timeout
**Solution**: Check network connectivity and FDA API status

## Resources

- [openFDA API Documentation](https://open.fda.gov/apis/)
- [Fivetran Connector SDK Docs](https://fivetran.com/docs/connectors/connector-sdk)
- [Fivetran API Reference](https://fivetran.com/docs/rest-api)

## License

MIT License - See LICENSE file for details


