# FDA Dashboard - Quick Start Guide

## 🌐 Deployed on Google Cloud Shell

> **This project is optimized for Google Cloud Shell!** No local setup needed - just open Cloud Shell and run.

## 🚀 5-Minute Setup (Cloud Shell - Recommended)

### Option 1: Google Cloud Shell ⭐ (Easiest)

```bash
# 1. Open Cloud Shell (click >_ icon in GCP Console)

# 2. Create project directory
mkdir -p ~/fda-intelligence-dashboard/streamlit_app
cd ~/fda-intelligence-dashboard/streamlit_app

# 3. Create the app file
nano app_final_v2.py
# (Paste the application code and save: Ctrl+X, Y, Enter)

# 4. Install dependencies (user install, no sudo needed)
pip install streamlit pandas google-cloud-bigquery google-cloud-translate \
  google-cloud-speech google-cloud-texttospeech plotly --user

# 5. Run the app
streamlit run app_final_v2.py --server.port 8501

# 6. Access via Web Preview
# Click "Web Preview" button → "Preview on port 8501"
```

**Cloud Shell Advantages:**
- ✅ Pre-authenticated (no credentials setup!)
- ✅ All GCP tools pre-installed
- ✅ Free to use
- ✅ Access from any browser
- ✅ 5GB persistent storage

### Keep Cloud Shell Running

```bash
# Use tmux to prevent timeouts
tmux new -s dashboard
streamlit run app_final_v2.py --server.port 8501

# Detach: Ctrl+B then D
# Reattach later: tmux attach -t dashboard
```

---

## 💻 Alternative: Local Setup

### Step 1: Install Dependencies
```bash
pip install streamlit pandas google-cloud-bigquery google-cloud-translate \
  google-cloud-speech google-cloud-texttospeech plotly --user
```

### Step 2: Set Up Authentication
```bash
gcloud auth application-default login
```

### Step 3: Grant Permissions
```bash
PROJECT_ID="fda-dashboard-1761298726"
SERVICE_ACCOUNT="fivetran-sa@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/bigquery.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/serviceusage.serviceUsageConsumer"
```

### Step 4: Run the App
```bash
streamlit run app_final_v2.py --server.port 8501
```

### Step 5: Configure
1. Open Web Preview (port 8501)
2. Enter Project ID: `fda-dashboard-1761298726`
3. Enter Dataset: `fda_data`
4. Click "Connect"

## 📖 First Time Using the App?

### 1️⃣ Start with Data Explorer
Go to **"🔍 Data Explorer"** tab to see:
- What drugs are in the database
- What reactions are available
- Sample data structure

### 2️⃣ Try a Search
Go to **"🔎 Search"** tab:
- Click a suggested drug/reaction button, OR
- Type a drug name from Data Explorer
- Click "Search"

### 3️⃣ Analyze a Drug
Go to **"💊 Drug Analysis"** tab:
- Click a suggested drug button, OR
- Enter drug name (e.g., "aspirin")
- Click "Analyze"
- View safety profile and risk assessment

## 🎯 Common Tasks

### Search for a Drug
```
1. Go to Data Explorer → Copy drug name
2. Go to Search → Paste drug name → Search
3. Download results as CSV
```

### Analyze Drug Safety
```
1. Go to Drug Analysis
2. Enter drug name
3. Review metrics and charts
4. Check risk assessment (High/Moderate/Low)
```

### Translate a Report
```
1. Go to Translation tab
2. Paste text
3. Select language
4. Click Translate
```

### Generate Audio Summary
```
1. Go to Voice tab → Text-to-Speech
2. Paste summary text
3. Click Generate
4. Download MP3
```

## ⚡ Quick Tips

✅ **Always check Data Explorer first** - Know what data is available  
✅ **Use single-word searches** - "aspirin" works better than "aspirin headache"  
✅ **Click suggestion buttons** - Faster than typing  
✅ **Download results** - Export to CSV for further analysis  
✅ **Check serious rate** - Key metric for drug safety  

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| No search results | Check Data Explorer for available terms |
| Permission errors | Run the `gcloud projects add-iam-policy-binding` commands |
| Slow queries | Reduce result limits, use specific search terms |
| Charts not showing | Refresh page, check data returned |

## 📞 Need Help?

- Read the full [README.md](README.md)
- Check available data in Data Explorer tab
- Verify data in BigQuery: `bq query "SELECT COUNT(*) FROM fda_data.fda_drug_adverse_events"`

## 🎉 You're Ready!

Start exploring FDA drug safety data! 🚀
