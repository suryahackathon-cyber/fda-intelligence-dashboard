# Quick Start Guide - Enhanced AI Dashboard

## 🚀 Get Started in 10 Minutes

This guide will help you set up the **Enhanced FDA Intelligence Dashboard** with all 8 Google Cloud AI features.

---

## Prerequisites

Before starting, ensure you have:

- ✅ Python 3.9 or higher
- ✅ Google Cloud Platform account ([Sign up](https://cloud.google.com/free))
- ✅ Fivetran account ([Free trial](https://fivetran.com/signup))
- ✅ FDA API key ([Get key](https://open.fda.gov/apis/authentication/))
- ✅ Git installed

---

## Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/fda-intelligence-dashboard.git
cd fda-intelligence-dashboard
```

---

## Step 2: Setup Google Cloud Platform

### A. Create GCP Project

```bash
# Set your project ID
export PROJECT_ID="your-fda-dashboard-project"

# Create project
gcloud projects create $PROJECT_ID

# Set as active project
gcloud config set project $PROJECT_ID

# Link billing account (required for AI APIs)
gcloud beta billing projects link $PROJECT_ID --billing-account=YOUR_BILLING_ACCOUNT_ID
```

### B. Enable Required APIs

```bash
# Enable all AI and data services
gcloud services enable \
    aiplatform.googleapis.com \
    bigquery.googleapis.com \
    language.googleapis.com \
    translate.googleapis.com \
    speech.googleapis.com \
    texttospeech.googleapis.com \
    storage-component.googleapis.com \
    compute.googleapis.com
```

This takes **2-3 minutes**.

### C. Create Service Account

```bash
# Create service account
gcloud iam service-accounts create fda-dashboard-sa \
    --display-name="FDA Dashboard Service Account"

# Grant necessary roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:fda-dashboard-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/bigquery.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:fda-dashboard-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:fda-dashboard-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/cloudtranslate.user"

# Download credentials
gcloud iam service-accounts keys create ~/fda-dashboard-key.json \
    --iam-account=fda-dashboard-sa@${PROJECT_ID}.iam.gserviceaccount.com

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/fda-dashboard-key.json"
```

### D. Create BigQuery Dataset

```bash
# Create dataset for FDA data
bq mk --dataset --location=US $PROJECT_ID:fda_data

# Set environment variable
export BQ_DATASET_ID="fda_data"
```

---

## Step 3: Deploy Fivetran Connector

### A. Install Connector Dependencies

```bash
cd fda_connector
pip install -r requirements.txt
```

### B. Test Connector Locally

```bash
# Test the connector
python test_connector.py
```

You should see output like:
```
✓ Schema test passed
✓ Data fetch test passed
✓ Update test passed
```

### C. Deploy to Fivetran

1. **Login to Fivetran Console**: https://fivetran.com/dashboard

2. **Create New Connector**:
   - Click "Add Connector"
   - Select "Function" (Custom connector)
   - Name: "FDA-Data-Connector"

3. **Upload Files**:
   - Upload `connector.py`
   - Upload `requirements.txt`
   - Set configuration from `configuration.json`

4. **Configure Connector**:
   ```json
   {
     "api_key": "YOUR_FDA_API_KEY",
     "endpoint": "drug_adverse_events",
     "start_date": "2023-01-01",
     "limit_per_request": 100
   }
   ```

5. **Select Destination**:
   - Choose "Google BigQuery"
   - Project: Your GCP project ID
   - Dataset: `fda_data`
   - Authenticate with your service account

6. **Start Sync**:
   - Click "Save & Test"
   - Start initial sync (takes 5-10 minutes)

---

## Step 4: Install Dashboard Dependencies

```bash
cd ../streamlit_app

# Install enhanced requirements
pip install -r requirements_enhanced.txt
```

---

## Step 5: Configure Environment

Create a `.env` file in `streamlit_app/`:

```bash
# Create .env file
cat > .env << EOF
GOOGLE_APPLICATION_CREDENTIALS=$HOME/fda-dashboard-key.json
GCP_PROJECT_ID=$PROJECT_ID
BQ_DATASET_ID=fda_data
GCP_LOCATION=us-central1
EOF
```

---

## Step 6: Run Enhanced Dashboard

```bash
# Run the enhanced dashboard
streamlit run app_enhanced.py
```

The dashboard will open in your browser at: **http://localhost:8501**

---

## Step 7: Explore AI Features

### 🔮 Predictive Analytics (BigQuery ML)

1. Navigate to **"Predictive Analytics"** tab
2. Click **"Train BigQuery ML Model"**
3. Wait 2-3 minutes for model training
4. Enter patient profile and click **"Predict Risk"**

### 🔍 Semantic Search (Vertex AI Embeddings)

1. Go to **"Semantic Search"** tab
2. Enter query: *"drugs causing heart problems"*
3. Click **"Semantic Search"**
4. View ranked results by similarity

### 🧠 NLP Analysis (Natural Language API)

1. Open **"NLP Analysis"** tab
2. Paste adverse event text
3. Click **"Analyze Text"**
4. View extracted entities and sentiment

### 🌐 Translation (Translation API)

1. Go to **"Translation"** tab
2. Enter drug safety text
3. Select target language (e.g., Spanish)
4. Click **"Translate"**

### 🎤 Voice Interface

1. Open **"Voice Interface"** tab
2. For **Speech-to-Text**:
   - Upload a WAV audio file
   - Click "Transcribe"
3. For **Text-to-Speech**:
   - Enter text
   - Click "Generate Speech"
   - Listen or download

### 🤖 AI Insights (Vertex AI Gemini)

1. Navigate to **"AI Insights"** tab
2. Ask question: *"What are the top drug safety concerns?"*
3. Click **"Get AI Insight"**
4. Read comprehensive AI-generated analysis
5. Optionally click **"Listen to Insight"** for audio

---

## Architecture Diagram

```
┌─────────────────────┐
│   FDA openFDA API   │
│   (Public Data)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Fivetran Custom   │
│     Connector       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   BigQuery          │◄──── BigQuery ML (Predictions)
│   (Data Warehouse)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐      ┌────────────────────────┐
│   Streamlit         │─────►│ Vertex AI Gemini       │
│   Dashboard         │      │ Vertex AI Embeddings   │
│   (Enhanced)        │─────►│ Natural Language API   │
│                     │      │ Translation API        │
│                     │─────►│ Speech-to-Text         │
│                     │      │ Text-to-Speech         │
└─────────────────────┘      └────────────────────────┘
```

---

## Verification Checklist

After completing all steps, verify:

- [ ] Fivetran connector syncing successfully
- [ ] BigQuery dataset contains FDA data
- [ ] Dashboard connects to GCP services
- [ ] All 7 tabs visible in dashboard
- [ ] Gemini AI responds to queries
- [ ] BigQuery ML model trains successfully
- [ ] Semantic search returns results
- [ ] NLP analysis extracts entities
- [ ] Translation works for selected languages
- [ ] Speech-to-Text transcribes audio
- [ ] Text-to-Speech generates audio

---

## Troubleshooting

### Issue: "Permission Denied" errors

**Solution**: Ensure service account has all required roles:
```bash
gcloud projects get-iam-policy $PROJECT_ID \
    --flatten="bindings[].members" \
    --filter="bindings.members:fda-dashboard-sa@*"
```

### Issue: "API not enabled"

**Solution**: Enable the missing API:
```bash
gcloud services enable [API_NAME].googleapis.com
```

### Issue: BigQuery ML model creation fails

**Solution**: Ensure you have sufficient data:
```bash
bq query --use_legacy_sql=false \
"SELECT COUNT(*) FROM \`$PROJECT_ID.fda_data.fda_drug_adverse_events\`"
```

Need at least 1,000 rows for model training.

### Issue: Embedding generation slow

**Solution**: This is normal for first run. Subsequent requests will be faster due to caching.

### Issue: Speech-to-Text not working

**Solution**: Ensure audio format is correct:
- Format: WAV
- Encoding: LINEAR16
- Sample rate: 16,000 Hz

---

## Cost Estimation

For **light usage** (testing/development):

| Service | Monthly Cost |
|---------|--------------|
| BigQuery Storage (100 GB) | $2.00 |
| BigQuery Queries | $1.00 |
| Vertex AI Gemini (1K requests) | $2.00 |
| BigQuery ML | $0.50 |
| Embeddings (5K) | $1.00 |
| Natural Language API (1K docs) | $1.00 |
| Translation (100K chars) | $2.00 |
| Speech-to-Text (100 min) | $0.24 |
| Text-to-Speech (100K chars) | $1.60 |
| **Total** | **~$11.34/month** |

**Free tier** covers most development usage!

---

## Next Steps

Now that your dashboard is running:

1. **Explore Data**: Navigate through all tabs
2. **Train Models**: Create custom BigQuery ML models
3. **Ask Questions**: Use Gemini for insights
4. **Customize**: Modify queries and visualizations
5. **Scale**: Sync more FDA endpoints
6. **Deploy**: Host on Cloud Run for production

---

## Production Deployment

To deploy to production:

```bash
# Build container
gcloud builds submit --tag gcr.io/$PROJECT_ID/fda-dashboard

# Deploy to Cloud Run
gcloud run deploy fda-dashboard \
    --image gcr.io/$PROJECT_ID/fda-dashboard \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars GCP_PROJECT_ID=$PROJECT_ID,BQ_DATASET_ID=fda_data
```

---

## Resources

- 📚 [Full Documentation](../README.md)
- 🤖 [AI Features Guide](GCP_AI_FEATURES.md)
- ❓ [FAQ](FAQ.md)
- 🐛 [GitHub Issues](https://github.com/YOUR_USERNAME/fda-intelligence-dashboard/issues)

---

## Support

Need help? 

- **Email**: your-email@example.com
- **GitHub**: Open an issue
- **Discord**: Join our community

---

**🎉 Congratulations! You now have a state-of-the-art AI-powered FDA intelligence dashboard!**

Built with ❤️ for the Fivetran × Google Cloud Challenge 2024

