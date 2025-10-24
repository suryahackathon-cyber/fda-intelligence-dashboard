# FDA Dashboard - Deployment Checklist

## 🌐 Cloud Shell Deployment (Recommended)

> This project is optimized for Google Cloud Shell deployment

### Cloud Shell Pre-Deployment Checklist

- [ ] Google Cloud Console access
- [ ] GCP Project created and selected
- [ ] Billing enabled on project
- [ ] You have necessary IAM permissions (Editor or Owner role)
- [ ] Cloud Shell activated (click >_ icon)

### Cloud Shell Advantages
- ✅ No authentication setup needed
- ✅ All GCP tools pre-installed
- ✅ Automatic credential management
- ✅ Free compute resources
- ✅ Web Preview for instant access
- ✅ 5GB persistent home directory

---

## 📋 Pre-Deployment

### Google Cloud Setup
- [ ] GCP Project created
- [ ] Billing enabled on project
- [ ] BigQuery API enabled
- [ ] Translation API enabled (optional)
- [ ] Speech-to-Text API enabled (optional)
- [ ] Text-to-Speech API enabled (optional)

### Data Setup
- [ ] BigQuery dataset `fda_data` created
- [ ] Table `fda_drug_adverse_events` created
- [ ] Data synced from openFDA API
- [ ] Verify data with: `bq query "SELECT COUNT(*) FROM fda_data.fda_drug_adverse_events"`
- [ ] Confirm data has both drug_names and reactions fields populated

### Authentication
- [ ] Service account created
- [ ] Service account key downloaded (if using key file)
- [ ] Application default credentials configured (if using ADC)
- [ ] `GOOGLE_APPLICATION_CREDENTIALS` environment variable set (if applicable)

### Permissions
- [ ] Service account has `roles/bigquery.admin`
- [ ] Service account has `roles/serviceusage.serviceUsageConsumer`
- [ ] Service account has `roles/cloudtranslate.user` (if using translation)
- [ ] Service account has `roles/speech.admin` (if using speech)
- [ ] Service account has `roles/texttospeech.admin` (if using TTS)

### Local Environment
- [ ] Python 3.8+ installed
- [ ] pip updated: `pip install --upgrade pip`
- [ ] Virtual environment created (recommended)
- [ ] All dependencies installed from requirements.txt

---

## 🚀 Deployment Steps

### 1. Copy Application Files
```bash
cd ~/fda-intelligence-dashboard/streamlit_app
# Copy app_final_v2.py to this directory
```

### 2. Install Requirements
```bash
pip install -r requirements.txt --user
```

### 3. Set Environment Variables
```bash
export GCP_PROJECT="fda-dashboard-1761298726"
export BQ_DATASET="fda_data"
```

### 4. Test Connection
```bash
# Test BigQuery access
bq query --use_legacy_sql=false "SELECT COUNT(*) FROM fda_data.fda_drug_adverse_events LIMIT 1"
```

### 5. Start Application
```bash
streamlit run app_final_v2.py --server.port 8501
```

### 6. Verify Startup
- [ ] App opens in browser
- [ ] No import errors in console
- [ ] Sidebar shows configuration options

### 7. Connect in UI
- [ ] Enter Project ID: `fda-dashboard-1761298726`
- [ ] Enter Dataset: `fda_data`
- [ ] Click "Connect to Google Cloud"
- [ ] Verify "✅ BigQuery connected" message
- [ ] Check for Translation/Speech API status

---

## ✅ Post-Deployment Verification

### Test Overview Tab
- [ ] Overview tab loads
- [ ] All 5 metric cards display numbers
- [ ] Top 20 drugs chart renders
- [ ] Top 20 reactions treemap renders
- [ ] No console errors

### Test Data Explorer Tab
- [ ] Table statistics display
- [ ] Top 50 drugs table loads
- [ ] Top 50 reactions table loads
- [ ] Sample data shows 10 rows
- [ ] Copyable lists work

### Test Search Tab
- [ ] Search box accepts input
- [ ] Quick suggestion buttons work
- [ ] Search returns results for known drug (e.g., "ASPIRIN")
- [ ] Summary statistics display
- [ ] CSV download works

### Test Drug Analysis Tab
- [ ] Drug name input works
- [ ] Quick drug buttons work
- [ ] Analysis displays for known drug
- [ ] All 5 metric cards show
- [ ] Reactions chart renders
- [ ] Trend chart renders
- [ ] Risk assessment box displays

### Test Translation Tab (Optional)
- [ ] Text area accepts input
- [ ] Language selector works
- [ ] Translation produces output
- [ ] Translated text is copyable

### Test Voice Tab (Optional)
- [ ] Speech-to-Text file uploader works
- [ ] Text-to-Speech text area accepts input
- [ ] Audio player displays
- [ ] Download button works

---

## 🔍 Health Checks

### Daily Checks
```bash
# 1. Check data freshness
bq query --use_legacy_sql=false "
SELECT MAX(fetched_at) as last_update 
FROM fda_data.fda_drug_adverse_events
"

# 2. Check record count
bq query --use_legacy_sql=false "
SELECT COUNT(*) as total_records 
FROM fda_data.fda_drug_adverse_events
"

# 3. Check app is running
curl -I http://localhost:8501
```

### Weekly Checks
- [ ] Review BigQuery usage and costs
- [ ] Check Translation API usage (if enabled)
- [ ] Check Speech API usage (if enabled)
- [ ] Review application logs
- [ ] Test all major features
- [ ] Verify data sync is working

---

## 🐛 Troubleshooting Checklist

### App Won't Start
- [ ] Check Python version: `python --version` (should be 3.8+)
- [ ] Verify all packages installed: `pip list | grep -E "streamlit|pandas|google-cloud"`
- [ ] Check for syntax errors: `python -m py_compile app_final_v2.py`
- [ ] Review error messages in console

### Can't Connect to BigQuery
- [ ] Verify project ID is correct
- [ ] Check authentication: `gcloud auth list`
- [ ] Verify service account has permissions
- [ ] Test direct BigQuery access: `bq ls fda_data`
- [ ] Check for typos in dataset/table names

### No Data Showing
- [ ] Confirm table has data: `bq query "SELECT COUNT(*) FROM fda_data.fda_drug_adverse_events"`
- [ ] Check data format in sample rows
- [ ] Verify drug_names and reactions fields are populated
- [ ] Review query logs for errors

### Search Returns No Results
- [ ] Go to Data Explorer to see available data
- [ ] Try simpler search terms (single words)
- [ ] Check spelling
- [ ] Verify search term exists in Data Explorer lists

### Charts Not Rendering
- [ ] Check browser console for JavaScript errors
- [ ] Verify Plotly version: `pip show plotly`
- [ ] Try different browser
- [ ] Check if query returned data

### Permission Errors
- [ ] Wait 60 seconds for IAM changes to propagate
- [ ] Re-run permission grant commands
- [ ] Check service account is correct
- [ ] Verify all required APIs are enabled

---

## 📊 Performance Monitoring

### Metrics to Track
- [ ] Query response times
- [ ] Page load times
- [ ] BigQuery bytes scanned
- [ ] Translation API calls (if applicable)
- [ ] Speech API calls (if applicable)
- [ ] Concurrent users
- [ ] Error rates

### Optimization Checklist
- [ ] Enable BigQuery table partitioning
- [ ] Use query result caching
- [ ] Implement Streamlit caching for expensive operations
- [ ] Limit result set sizes
- [ ] Monitor and optimize slow queries

---

## 🔒 Security Checklist

### Before Production
- [ ] Service account key file secured (not in git)
- [ ] Environment variables set properly
- [ ] IAM permissions follow least privilege
- [ ] Audit logging enabled
- [ ] Data encryption at rest enabled
- [ ] VPC controls configured (if applicable)
- [ ] API keys secured
- [ ] No hardcoded credentials in code

### Regular Security Tasks
- [ ] Rotate service account keys (quarterly)
- [ ] Review IAM permissions (monthly)
- [ ] Check access logs (weekly)
- [ ] Update dependencies (monthly)
- [ ] Review security advisories

---

## 📝 Documentation Checklist

### User Documentation
- [ ] README.md is up to date
- [ ] QUICKSTART.md is accurate
- [ ] Screenshots are current
- [ ] API reference is complete
- [ ] Troubleshooting section is comprehensive

### Technical Documentation
- [ ] Code is commented
- [ ] Architecture diagram is current
- [ ] Data model is documented
- [ ] Deployment process is documented
- [ ] Runbook for common issues exists

---

## 🎯 Go-Live Checklist

### Final Checks Before Launch
- [ ] All tests pass
- [ ] Performance is acceptable
- [ ] Security review complete
- [ ] Documentation complete
- [ ] Backup and recovery tested
- [ ] Monitoring configured
- [ ] Support team trained
- [ ] Users notified of launch

### Launch Day
- [ ] Deploy during low-usage period
- [ ] Monitor logs closely
- [ ] Be available for support
- [ ] Document any issues
- [ ] Communicate with stakeholders

### Post-Launch
- [ ] Monitor for 24 hours
- [ ] Gather user feedback
- [ ] Address critical issues immediately
- [ ] Plan next iteration
- [ ] Update documentation with lessons learned

---

## ✅ Sign-Off

Deployment completed by: ___________________  
Date: ___________________  
Verified by: ___________________  

Notes:
_____________________________________________
_____________________________________________
_____________________________________________

---

**Ready to deploy? Go through this checklist step by step!** ✨
