# Frequently Asked Questions (FAQ)

## General Questions

### What is the FDA Intelligence Dashboard?

The FDA Intelligence Dashboard is an AI-powered platform that automatically syncs FDA drug safety data (adverse events, recalls, labels) through a custom Fivetran connector to Google Cloud BigQuery, then provides intelligent insights using Vertex AI Gemini through an interactive Streamlit dashboard.

### Who is this for?

- Healthcare providers seeking drug safety insights
- Patients researching medication safety
- Researchers analyzing adverse event patterns
- Data scientists building healthcare applications
- Hackathon participants for the Fivetran × Google Cloud Challenge

### Is this free to use?

Yes! The project is open source under MIT license. Cloud costs depend on usage:
- Google Cloud offers $300 free trial credits
- Fivetran offers 14-day free trial
- After trials, expect $10-50/month depending on usage

---

## Technical Questions

### What data does the connector sync?

The connector can sync from 5 FDA endpoints:
1. **Drug Adverse Events**: Reports of adverse reactions
2. **Drug Labels**: Official drug labeling information  
3. **Drug Recalls**: Drug product recalls
4. **Food Recalls**: Food product recalls
5. **Device Adverse Events**: Medical device events

All data comes from the public [openFDA API](https://open.fda.gov/).

### How often does data sync?

Default is every 24 hours. You can configure sync frequency in Fivetran from hourly to weekly based on your needs and rate limits.

### Do I need an FDA API key?

Not required, but highly recommended:
- **Without key**: 240 requests/minute, 1,000/day
- **With key**: 240 requests/minute, 120,000/day

Get a free key instantly at: https://open.fda.gov/apis/authentication/

### What Google Cloud services are required?

- **BigQuery**: Data warehouse (required)
- **Vertex AI**: Gemini models for AI insights (required)
- **Cloud Run**: For deployment (optional)
- **IAM**: Service accounts for authentication (required)

### Can I use this without Fivetran?

The connector is specifically built for Fivetran's SDK. However, you could adapt the core FDA API logic to work standalone or with other ETL tools.

---

## Setup Questions

### I'm getting authentication errors in GCP

**Common solutions**:

1. **Verify credentials are set**:
   ```bash
   echo $GOOGLE_APPLICATION_CREDENTIALS
   # Should show path to your JSON key file
   ```

2. **Check key file exists**:
   ```bash
   cat $GOOGLE_APPLICATION_CREDENTIALS
   # Should show JSON content
   ```

3. **Re-authenticate**:
   ```bash
   gcloud auth application-default login
   ```

4. **Verify service account permissions**:
   - Go to: GCP Console → IAM & Admin → IAM
   - Check your service account has required roles:
     - `BigQuery Data Viewer`
     - `BigQuery Job User`
     - `Vertex AI User`

### Fivetran says "Connection failed" to BigQuery

**Check these**:

1. **Service account JSON is valid**:
   - Re-download key from GCP
   - Ensure entire JSON content is uploaded

2. **Service account has permissions**:
   ```bash
   gcloud projects add-iam-policy-binding PROJECT_ID \
     --member="serviceAccount:fivetran-sa@PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/bigquery.dataEditor"
   ```

3. **BigQuery API is enabled**:
   ```bash
   gcloud services enable bigquery.googleapis.com
   ```

4. **Dataset exists**:
   ```bash
   bq ls PROJECT_ID:fda_data
   ```

### Dashboard shows "No data available"

**Troubleshooting steps**:

1. **Check Fivetran sync status**:
   - Go to Fivetran dashboard
   - View connector status
   - Check sync history for errors

2. **Verify data in BigQuery**:
   ```bash
   bq query --use_legacy_sql=false \
     'SELECT COUNT(*) FROM `PROJECT_ID.fda_data.fda_drug_adverse_events`'
   ```

3. **Check dashboard configuration**:
   - Correct Project ID?
   - Correct Dataset ID (`fda_data`)?
   - Service account has read permissions?

4. **View logs**:
   ```bash
   # Streamlit logs
   streamlit run app.py --logger.level=debug
   ```

### AI Insights not working

**Solutions**:

1. **Enable Vertex AI API**:
   ```bash
   gcloud services enable aiplatform.googleapis.com
   ```

2. **Check service account role**:
   ```bash
   gcloud projects add-iam-policy-binding PROJECT_ID \
     --member="serviceAccount:SA_EMAIL" \
     --role="roles/aiplatform.user"
   ```

3. **Verify region supports Gemini**:
   - Use: `us-central1`, `us-east1`, or `europe-west1`
   - Change in dashboard sidebar

4. **Test Vertex AI access**:
   ```bash
   gcloud ai models list --region=us-central1
   ```

---

## Connector Questions

### How do I test the connector locally?

```bash
cd fda_connector
pip install -r requirements.txt
python test_connector.py
```

This fetches sample data without deploying to Fivetran.

### Can I sync multiple FDA endpoints?

Yes! Deploy separate connector instances for each endpoint:
- `FDA-Drug-Adverse-Events` → `drug_adverse_events`
- `FDA-Drug-Recalls` → `drug_recalls`
- `FDA-Food-Recalls` → `food_recalls`

Each creates a separate table in the same BigQuery dataset.

### How do I handle rate limiting?

**Solutions**:

1. **Get FDA API key** (recommended)
2. **Reduce `limit_per_request`** to 50-100
3. **Increase sync frequency** to avoid large batches
4. **Contact FDA** for higher rate limits (enterprise)

The connector has built-in rate limiting with automatic retries.

### Can I customize the data schema?

Yes! Edit the `schema()` method in `connector.py`:

```python
def schema(self) -> Dict[str, Any]:
    return {
        "table": "my_custom_table_name",
        "primary_key": ["my_key"],
        "columns": {
            "my_field": "STRING",
            # Add more fields...
        }
    }
```

Redeploy the connector after changes.

---

## Deployment Questions

### Where can I deploy the dashboard?

**Options**:

1. **Google Cloud Run** (recommended):
   - Serverless, auto-scaling
   - Pay only for usage
   - Built-in HTTPS

2. **Streamlit Cloud**:
   - Free tier available
   - Automatic deployments from GitHub
   - Easy secret management

3. **Local/VPS**:
   - Full control
   - Manual management
   - For internal use

See [Deployment Guide](DEPLOYMENT_GUIDE.md) for instructions.

### How do I make the dashboard public?

**For Cloud Run**:
```bash
gcloud run deploy fda-dashboard --allow-unauthenticated
```

**For Streamlit Cloud**:
- Deploy with public repository
- Dashboard is automatically public

**Security note**: Don't expose sensitive credentials in public dashboards.

### How do I add authentication?

**Option 1: Google Identity-Aware Proxy (IAP)**:
```bash
gcloud iap web enable \
  --resource-type=app-engine \
  --service=fda-dashboard
```

**Option 2: Streamlit Authentication**:
```python
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(config)
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # Show dashboard
```

**Option 3: OAuth with Google**:
- Use `streamlit-oauth` library
- Configure OAuth credentials in GCP Console

---

## Cost Questions

### How much will this cost?

**Conservative estimate**:

**Fivetran** (after 14-day trial):
- ~$50-100/month (depends on row volume)
- Free trial covers development period

**Google Cloud** (free tier eligible):
- BigQuery storage: ~$0-2/month (first 10GB free)
- BigQuery queries: ~$0-3/month (first 1TB free)
- Vertex AI: ~$0-2/month (Gemini Flash is cheap)
- Cloud Run: ~$0-5/month (free tier: 2M requests)

**Total**: ~$0-12/month (GCP only, within free tier)

### How do I reduce costs?

**Strategies**:

1. **BigQuery**:
   - Use `LIMIT` in queries
   - Select only needed columns
   - Use date partitioning
   - Set table expiration for old data

2. **Vertex AI**:
   - Use Gemini Flash instead of Pro
   - Cache common queries
   - Limit response length
   - Rate limit AI requests

3. **Fivetran**:
   - Reduce sync frequency
   - Sync only needed endpoints
   - Use date filters in connector

4. **Cloud Run**:
   - Set max instances limit
   - Use smaller container image
   - Enable concurrency

### Can I use only the free tier?

Yes! For the hackathon period:
- Google Cloud: $300 free trial credits (90 days)
- Fivetran: 14-day free trial
- This is enough to build and demo the project

For longer-term use, you'll need to monitor and optimize costs.

---

## Data Questions

### How current is the data?

FDA updates their API daily. Your data freshness depends on:
- Fivetran sync frequency (default: 24 hours)
- FDA's update schedule (varies by endpoint)
- Your `start_date` configuration

Recent events typically appear within 24-48 hours.

### Is patient data included?

No personally identifiable information (PII) is included. The data is:
- De-identified
- Aggregated
- Public domain
- Compliant with HIPAA (no PHI)

### Can I export the data?

Yes! Multiple ways:

1. **From BigQuery**:
   ```bash
   bq extract --destination_format CSV \
     'PROJECT_ID:fda_data.fda_drug_adverse_events' \
     gs://YOUR_BUCKET/export.csv
   ```

2. **From Dashboard**:
   - Use Streamlit's download button (add to app)
   - Or query and save manually

3. **Direct API**:
   - Query BigQuery REST API
   - Use BigQuery client libraries

### How far back does the data go?

Depends on your `start_date` configuration:
- Default: All available data
- FDA has data from early 2000s for most endpoints
- More recent data is more complete and standardized

---

## AI Questions

### What AI model is used?

**Gemini 1.5 Flash** via Google Vertex AI:
- Fast responses (< 10 seconds)
- Cost-effective ($0.00001875 per 1K input characters)
- 1M token context window
- Multimodal capable

You can switch to Gemini Pro for more complex analysis.

### How accurate are the AI insights?

The AI provides:
- Pattern recognition from data
- Contextual analysis
- Evidence-based recommendations

**Important**: AI insights are supplementary to professional medical advice. Always consult healthcare providers for medical decisions.

### Can I customize AI prompts?

Yes! Edit the prompts in `app.py`:

```python
def analyze_with_gemini(self, data_summary: str, question: str) -> str:
    prompt = f"""
    Your custom prompt here...
    
    Data: {data_summary}
    Question: {question}
    """
    # ... rest of code
```

Redeploy after changes.

### Does the AI access external data?

No. The AI only analyzes:
1. Data from your BigQuery tables
2. Context provided in prompts
3. No external API calls or web searches

This ensures data privacy and consistency.

---

## Troubleshooting

### Connector deployment fails

**Check**:
- Python syntax is valid: `python -m py_compile connector.py`
- All dependencies in `requirements.txt`
- Configuration JSON is valid: `python -m json.tool configuration.json`
- Fivetran CLI is latest version: `pip install --upgrade fivetran-connector-sdk`

### Dashboard is slow

**Optimizations**:

1. **Add caching**:
   ```python
   @st.cache_data(ttl=3600)
   def get_data():
       # Query logic
   ```

2. **Optimize queries**:
   - Use `LIMIT`
   - Add WHERE clauses
   - Create materialized views

3. **Reduce AI calls**:
   - Cache AI responses
   - Debounce user input

4. **Use Cloud Run with more resources**:
   ```bash
   gcloud run deploy --memory 4Gi --cpu 4
   ```

### "Module not found" errors

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Or use virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Challenge-Specific Questions

### Does this meet all challenge requirements?

Yes! ✅
- Custom Fivetran connector using SDK
- Syncs to Google Cloud BigQuery
- Uses Google Cloud AI (Vertex AI)
- Relevant to modern AI/data (RAG, agentic insights)
- Open source with license
- Production-ready

### What makes this project stand out?

**Innovation**:
- Real healthcare impact
- Novel use of FDA data
- AI-powered insights
- Beautiful UI/UX

**Technical Excellence**:
- Production-ready code
- Comprehensive documentation
- Error handling and logging
- Scalable architecture

**Completeness**:
- Full deployment guides
- Video demo
- Open source
- Easy to replicate

### Can I fork and modify this?

Absolutely! The project is MIT licensed:
- Fork the repository
- Modify as needed
- Give credit (appreciated but not required)
- Share your improvements!

---

## Support

Still have questions?

- 📖 **Documentation**: See [README.md](../README.md)
- 🐛 **Issues**: [Create an issue](https://github.com/YOUR_USERNAME/fda-intelligence-dashboard/issues)
- 💬 **Discussions**: Use GitHub Discussions
- 📧 **Email**: your.email@example.com

---

**Don't see your question? [Add it to our FAQ](https://github.com/YOUR_USERNAME/fda-intelligence-dashboard/issues/new?template=faq.md)**


