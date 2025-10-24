# 🚀 Quick Start Guide

Get the FDA Intelligence Dashboard running in 15 minutes!

## Prerequisites

- [ ] Python 3.9+ installed
- [ ] Google Cloud account ([Get $300 free credit](https://cloud.google.com/free))
- [ ] Fivetran account ([14-day free trial](https://fivetran.com/signup))

---

## Step 1: Google Cloud Setup (5 minutes)

### Create Project & Enable APIs

```bash
# Install gcloud CLI (if not already installed)
# Visit: https://cloud.google.com/sdk/docs/install

# Login to GCP
gcloud auth login

# Create new project
gcloud projects create fda-dashboard-$(date +%s) --name="FDA Dashboard"

# Set project
export PROJECT_ID="YOUR_PROJECT_ID_FROM_ABOVE"
gcloud config set project $PROJECT_ID

# Enable billing (required)
# Visit: https://console.cloud.google.com/billing
# Link a billing account to your project

# Enable required APIs
gcloud services enable bigquery.googleapis.com \
  aiplatform.googleapis.com \
  cloudresourcemanager.googleapis.com \
  iam.googleapis.com
```

### Create BigQuery Dataset

```bash
# Create dataset
bq mk --dataset --location=US $PROJECT_ID:fda_data

# Verify
bq ls
```

### Create Service Account

```bash
# Create service account
gcloud iam service-accounts create fda-dashboard-sa \
  --display-name="FDA Dashboard Service Account"

# Grant permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:fda-dashboard-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataViewer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:fda-dashboard-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/bigquery.jobUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:fda-dashboard-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

# Create and download key
gcloud iam service-accounts keys create ~/fda-dashboard-key.json \
  --iam-account=fda-dashboard-sa@$PROJECT_ID.iam.gserviceaccount.com

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/fda-dashboard-key.json"
export GCP_PROJECT_ID=$PROJECT_ID
export BQ_DATASET_ID="fda_data"
```

---

## Step 2: Fivetran Setup (5 minutes)

### Get FDA API Key

1. Visit: https://open.fda.gov/apis/authentication/
2. Fill out form → Get API key instantly
3. Save key: `export FDA_API_KEY="your_key_here"`

### Create Fivetran Service Account

```bash
# Create service account for Fivetran
gcloud iam service-accounts create fivetran-sa \
  --display-name="Fivetran Service Account"

# Grant BigQuery write permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:fivetran-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:fivetran-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/bigquery.jobUser"

# Create key for Fivetran
gcloud iam service-accounts keys create ~/fivetran-key.json \
  --iam-account=fivetran-sa@$PROJECT_ID.iam.gserviceaccount.com
```

### Setup Fivetran (Manual Steps)

1. **Sign up**: https://fivetran.com/signup
2. **Add BigQuery Destination**:
   - Go to: Destinations → + Destination
   - Select: BigQuery
   - Upload: `~/fivetran-key.json`
   - Project ID: `$PROJECT_ID`
   - Dataset: `fda_data`

3. **Deploy FDA Connector**:
   ```bash
   cd fda_connector
   zip -r fda_connector.zip connector.py configuration.json requirements.txt
   ```
   - Upload to Fivetran Custom Connectors
   - Configure: Choose endpoint (e.g., drug_adverse_events)
   - Add FDA API key
   - Start sync

---

## Step 3: Run Dashboard (5 minutes)

### Install & Run

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/fda-intelligence-dashboard.git
cd fda-intelligence-dashboard

# Setup dashboard
cd streamlit_app
pip install -r requirements.txt

# Make sure environment variables are set
echo $GOOGLE_APPLICATION_CREDENTIALS  # Should show path to key
echo $GCP_PROJECT_ID                  # Should show project ID
echo $BQ_DATASET_ID                   # Should show fda_data

# Run dashboard
streamlit run app.py
```

### Access Dashboard

1. Opens automatically at: `http://localhost:8501`
2. In sidebar, verify connection settings:
   - GCP Project ID: (auto-filled from env var)
   - BigQuery Dataset: `fda_data`
3. Click "Connect to Google Cloud"
4. Explore the data!

---

## Verification Checklist

- [ ] BigQuery dataset `fda_data` exists
- [ ] Fivetran sync is running (check Fivetran dashboard)
- [ ] Dashboard connects without errors
- [ ] Overview tab shows metrics
- [ ] AI Insights tab responds to questions

---

## Troubleshooting

### No data in dashboard?
```bash
# Check if Fivetran has synced data
bq query --use_legacy_sql=false \
  "SELECT COUNT(*) FROM \`$PROJECT_ID.fda_data.fda_drug_adverse_events\`"

# Should return > 0 rows
```

### Authentication errors?
```bash
# Verify credentials
gcloud auth application-default login

# Or check environment variable
echo $GOOGLE_APPLICATION_CREDENTIALS
```

### AI Insights not working?
```bash
# Verify Vertex AI is enabled
gcloud services list --enabled | grep aiplatform

# If not enabled:
gcloud services enable aiplatform.googleapis.com
```

---

## Next Steps

1. ✅ **Explore the Dashboard**: Try different tabs and features
2. 📊 **Add More Endpoints**: Deploy connectors for drug_recalls, drug_labels
3. 🚀 **Deploy to Cloud**: Follow [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
4. 🎥 **Create Demo Video**: Record your solution for submission
5. 📤 **Submit to Devpost**: Complete your challenge submission

---

## Full Documentation

For detailed guides, see:
- [GCP Setup Guide](docs/GCP_SETUP.md)
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- [Connector Documentation](fda_connector/README.md)
- [Dashboard Documentation](streamlit_app/README.md)

---

## Need Help?

- 📖 Check the [full documentation](README.md)
- 🐛 [Create an issue](https://github.com/YOUR_USERNAME/fda-intelligence-dashboard/issues)
- 💬 Ask in challenge forums

---

**Ready? Let's build! 🚀**


