# 🌐 Google Cloud Shell Deployment Guide

## Why Cloud Shell for This Project?

This FDA Intelligence Dashboard was **specifically designed and optimized** for deployment on Google Cloud Shell, making it the easiest way to get started with zero local setup.

### ⭐ Key Benefits

| Feature | Benefit |
|---------|---------|
| **Zero Setup Time** | No Python, gcloud, or tools installation needed |
| **Pre-Authenticated** | Automatic GCP credentials - just works! |
| **Always Available** | Access from any device with a browser |
| **Cost-Free** | Completely free to use, included in GCP |
| **Team Ready** | Everyone gets the same environment |
| **Secure by Default** | Built-in security, no keys to manage |

---

## 🚀 Complete Cloud Shell Tutorial

### Step 1: Open Cloud Shell (30 seconds)

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project: **fda-dashboard-1761298726**
3. Click the **Cloud Shell** icon `>_` in the top-right corner
4. Wait for Cloud Shell to initialize (takes ~10 seconds)

You'll see a terminal at the bottom of your screen:
```
Welcome to Cloud Shell! Type "help" to get started.
username@cloudshell:~$
```

---

### Step 2: Create Project Directory (1 minute)

```bash
# Navigate to home directory (files here persist)
cd ~

# Create project structure
mkdir -p fda-intelligence-dashboard/streamlit_app
cd fda-intelligence-dashboard/streamlit_app

# Verify location
pwd
# Output: /home/your_username/fda-intelligence-dashboard/streamlit_app
```

**Why this matters:** Only files in your home directory (`~`) persist across Cloud Shell sessions!

---

### Step 3: Create Application File (2 minutes)

**Method A: Using Cloud Shell Editor (Recommended)**

1. Click **"Open Editor"** button at top of Cloud Shell
2. Navigate to `fda-intelligence-dashboard/streamlit_app/`
3. Right-click → **"New File"**
4. Name it: `app_final_v2.py`
5. Paste the application code
6. Save: `Ctrl+S` (Windows/Linux) or `Cmd+S` (Mac)
7. Click **"Open Terminal"** to return to terminal

**Method B: Using nano (Terminal)**

```bash
# Open nano editor
nano app_final_v2.py

# Paste the application code
# (Right-click → Paste, or Ctrl+Shift+V)

# Save and exit
# Press: Ctrl+X
# Then: Y (yes, save)
# Then: Enter (confirm filename)
```

---

### Step 4: Install Dependencies (1 minute)

```bash
# Install Python packages
pip install streamlit pandas google-cloud-bigquery \
  google-cloud-translate google-cloud-speech \
  google-cloud-texttospeech plotly --user
```

**Note:** 
- Use `--user` flag (no sudo needed or available)
- Installation takes ~30-60 seconds
- You'll see "Successfully installed..." messages

**Verify Installation:**
```bash
pip list | grep -E "streamlit|pandas|google-cloud|plotly"
```

---

### Step 5: Run the Application (30 seconds)

```bash
streamlit run app_final_v2.py --server.port 8501
```

**What you'll see:**
```
You can now view your Streamlit app in your browser.

Network URL: http://172.17.0.2:8501
External URL: http://35.xxx.xxx.xxx:8501
```

**Note:** Ignore these URLs - they won't work directly. Use Web Preview instead!

---

### Step 6: Access via Web Preview (30 seconds)

1. Look for **"Web Preview"** button (square with arrow icon) in Cloud Shell toolbar
2. Click it
3. Select **"Preview on port 8501"**
4. Your dashboard opens in a new browser tab!

**URL Format:** 
```
https://8501-cs-xxxxxxxxxxxxx-default.cs-us-central1-vfsd.cloudshell.dev
```

**Bookmark this URL** - it's unique to your session!

---

## 🎯 First-Time Usage

### Configure the Dashboard

Once the app opens:

1. **Sidebar Configuration:**
   - Project ID: `fda-dashboard-1761298726` (already filled)
   - Dataset ID: `fda_data` (already filled)

2. **Click "🔗 Connect to Google Cloud"**

3. **Wait for connection messages:**
   ```
   ✅ BigQuery connected
   ✅ Translation API connected
   ✅ Speech APIs connected
   ```

4. **Start exploring!** 🎉

---

## 💡 Cloud Shell Tips & Tricks

### Keep Your Session Alive

Cloud Shell times out after **20 minutes of inactivity**. Use `tmux`:

```bash
# Start a new tmux session
tmux new -s dashboard

# Run your app inside tmux
streamlit run app_final_v2.py --server.port 8501

# Detach from tmux (keeps running in background)
# Press: Ctrl+B, then D

# Reconnect later
tmux attach -t dashboard

# List all tmux sessions
tmux ls

# Kill a tmux session (when done)
tmux kill-session -t dashboard
```

---

### Boost Cloud Shell (More Resources)

Need more RAM or CPU?

1. Click **"More"** (⋮) in Cloud Shell toolbar
2. Select **"Boost Cloud Shell"**
3. Confirm boost (lasts 24 hours)

**Benefits:**
- More RAM (from 1.7GB to 8GB)
- More CPU cores
- Better performance for large queries

---

### Use Cloud Shell Editor

Full-featured IDE in your browser:

```bash
# Open editor from terminal
cloudshell edit app_final_v2.py

# Or click "Open Editor" button in toolbar
```

**Features:**
- Syntax highlighting
- Auto-completion
- Git integration
- Multi-file editing
- Terminal integrated

---

### File Management

```bash
# Upload files to Cloud Shell
# Click "More" (⋮) → "Upload file"

# Download files from Cloud Shell
# Click "More" (⋮) → "Download file"

# Or use gcloud storage
gsutil cp local-file.csv gs://your-bucket/
gsutil cp gs://your-bucket/file.csv ./
```

---

### Restart Streamlit Without Closing

If you make code changes:

```bash
# In the terminal running Streamlit, press:
Ctrl+C  # Stops Streamlit

# Then restart:
streamlit run app_final_v2.py --server.port 8501
```

Or use Streamlit's auto-reload (usually automatic when you save files).

---

## 🔧 Troubleshooting Cloud Shell

### Issue 1: "Files disappeared!"

**Cause:** Files not in home directory

**Solution:**
```bash
# Always work in home directory
cd ~
pwd
# Should show: /home/your_username

# Move files if needed
mv /tmp/myfiles ~/fda-intelligence-dashboard/
```

---

### Issue 2: "Web Preview shows error"

**Cause:** App not running or wrong port

**Solution:**
```bash
# 1. Check if Streamlit is running
ps aux | grep streamlit

# 2. Check port
netstat -tuln | grep 8501

# 3. Restart app
streamlit run app_final_v2.py --server.port 8501

# 4. Try different port if needed
streamlit run app_final_v2.py --server.port 8080
# Then use "Change port" in Web Preview
```

---

### Issue 3: "Session timed out"

**Cause:** 20 minutes of inactivity

**Solution:**
```bash
# Use tmux (as shown above)
# Or: Keep tab active and interact regularly
```

---

### Issue 4: "Out of memory"

**Cause:** Large queries or data processing

**Solutions:**
1. **Boost Cloud Shell** (see above)
2. Reduce result limits in the app
3. Use pagination
4. Clear browser cache

---

### Issue 5: "Permission denied"

**Cause:** Need to grant service account permissions

**Solution:**
```bash
PROJECT_ID="fda-dashboard-1761298726"
SERVICE_ACCOUNT="fivetran-sa@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/bigquery.admin"

# Wait 60 seconds for propagation
sleep 60
```

---

## 🎓 Best Practices

### 1. Always Use Home Directory
```bash
# ✅ Good
cd ~/fda-intelligence-dashboard
# Files persist here

# ❌ Bad
cd /tmp
# Files deleted on restart!
```

### 2. Use tmux for Long Sessions
```bash
# ✅ Good
tmux new -s dashboard
streamlit run app_final_v2.py --server.port 8501

# ❌ Bad
streamlit run app_final_v2.py --server.port 8501
# Times out after 20 min if inactive
```

### 3. Boost When Needed
```bash
# ✅ For heavy workloads
# Click "Boost Cloud Shell" before starting

# ❌ Don't boost unnecessarily
# Standard is fine for most operations
```

### 4. Clean Up When Done
```bash
# Stop Streamlit
Ctrl+C

# Kill tmux session
tmux kill-session -t dashboard

# (Optional) Clear pip cache to save space
pip cache purge
```

---

## 📊 Monitoring Your Cloud Shell Usage

### Check Resource Usage

```bash
# Memory usage
free -h

# Disk usage
df -h ~

# Running processes
top
# Press 'q' to quit
```

### Cloud Shell Quotas

| Resource | Limit | Notes |
|----------|-------|-------|
| **Persistent Storage** | 5 GB | Home directory |
| **RAM (Standard)** | 1.7 GB | Can be boosted to 8 GB |
| **Weekly Usage** | 50 hours | Resets weekly |
| **Session Timeout** | 20 min | Use tmux to prevent |

---

## 🚀 Advanced: Auto-Start on Cloud Shell Open

Create a startup script:

```bash
# Create startup script
nano ~/start-dashboard.sh
```

**Content:**
```bash
#!/bin/bash
cd ~/fda-intelligence-dashboard/streamlit_app
tmux new -d -s dashboard 'streamlit run app_final_v2.py --server.port 8501'
echo "Dashboard started in tmux session 'dashboard'"
echo "Access via Web Preview on port 8501"
echo "Attach to session: tmux attach -t dashboard"
```

**Make executable:**
```bash
chmod +x ~/start-dashboard.sh
```

**Run on startup:**
```bash
# Add to .bashrc
echo '~/start-dashboard.sh' >> ~/.bashrc
```

Now your dashboard auto-starts when you open Cloud Shell!

---

## 🌟 Cloud Shell vs Other Deployment Options

| Feature | Cloud Shell | Local Dev | Cloud Run | Compute Engine |
|---------|------------|-----------|-----------|----------------|
| **Setup Time** | 5 min | 30 min | 20 min | 30 min |
| **Cost** | Free | Free | $$ | $$$ |
| **Persistent** | Yes (5GB) | Yes | Yes | Yes |
| **Auto-scale** | No | No | Yes | Manual |
| **Best For** | Development, POC | Local dev | Production | Large-scale |

**Recommendation:**
- **Development/Testing**: Cloud Shell ⭐
- **Production**: Cloud Run
- **Enterprise**: Cloud Run + Load Balancer

---

## 📞 Getting Help

### Cloud Shell Documentation
- [Official Cloud Shell Docs](https://cloud.google.com/shell/docs)
- [Cloud Shell Limits](https://cloud.google.com/shell/docs/quotas)
- [Troubleshooting Guide](https://cloud.google.com/shell/docs/troubleshooting)

### Project-Specific Help
- Check [README.md](README.md) for full documentation
- See [QUICKSTART.md](QUICKSTART.md) for quick reference
- Review [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for deployment

### Common Commands Reference
```bash
# Cloud Shell
cloudshell dl file.txt          # Download file
cloudshell edit app.py           # Open editor
cloudshell boost                 # Boost resources

# Session Management
tmux new -s name                 # New session
tmux attach -t name              # Attach to session
tmux ls                          # List sessions
tmux kill-session -t name        # Kill session

# App Management
streamlit run app.py --server.port 8501    # Start app
Ctrl+C                                      # Stop app
ps aux | grep streamlit                     # Check if running
```

---

## ✅ Cloud Shell Checklist

### Initial Setup
- [ ] Open Cloud Shell
- [ ] Create project directory in home (`~`)
- [ ] Create `app_final_v2.py` file
- [ ] Install dependencies with `--user` flag
- [ ] Run app on port 8501
- [ ] Access via Web Preview

### Session Management
- [ ] Start tmux session for persistence
- [ ] Boost Cloud Shell if needed
- [ ] Save files in home directory
- [ ] Keep Web Preview URL bookmarked

### Regular Maintenance
- [ ] Check disk usage: `df -h ~`
- [ ] Clear pip cache: `pip cache purge`
- [ ] Update dependencies: `pip install --upgrade streamlit pandas`
- [ ] Kill unused tmux sessions

---

## 🎉 You're Ready!

You now know everything about deploying the FDA Dashboard on Google Cloud Shell!

**Quick Start Command:**
```bash
cd ~/fda-intelligence-dashboard/streamlit_app && \
tmux new -d -s dashboard 'streamlit run app_final_v2.py --server.port 8501' && \
echo "✅ Dashboard started! Access via Web Preview on port 8501"
```

---

**Happy Cloud Shelling!** ☁️🚀

*Last Updated: October 24, 2025*
