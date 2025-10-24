# Git Repository Setup Guide

Complete guide to push your FDA Intelligence Dashboard to GitHub.

## Prerequisites

- [ ] Git installed on your computer
- [ ] GitHub account created

### Install Git (if needed)

**Windows**:
```powershell
# Download from: https://git-scm.com/download/win
# Or use winget:
winget install -e --id Git.Git
```

**Verify Installation**:
```bash
git --version
# Should show: git version 2.x.x
```

---

## Step 1: Create GitHub Repository

### Option A: Using GitHub Website

1. **Go to GitHub**: https://github.com
2. **Sign in** to your account
3. **Click** the "+" icon (top-right) → "New repository"
4. **Configure Repository**:
   - **Repository name**: `fda-intelligence-dashboard`
   - **Description**: `AI-powered FDA data insights using Fivetran, BigQuery & Vertex AI`
   - **Visibility**: ✅ **Public** (required for open source)
   - **Initialize**: ❌ **DO NOT** check any boxes (no README, no .gitignore, no license)
     - We already have these files!
5. **Click** "Create repository"
6. **Copy** the repository URL:
   - HTTPS: `https://github.com/YOUR_USERNAME/fda-intelligence-dashboard.git`
   - SSH: `git@github.com:YOUR_USERNAME/fda-intelligence-dashboard.git`

### Option B: Using GitHub CLI (Optional)

```bash
# Install GitHub CLI
winget install --id GitHub.cli

# Login
gh auth login

# Create repository
gh repo create fda-intelligence-dashboard --public --description "AI-powered FDA data insights using Fivetran, BigQuery & Vertex AI"
```

---

## Step 2: Initialize Local Git Repository

Open PowerShell or Command Prompt and navigate to your project:

```powershell
# Navigate to project directory
cd C:\Users\SuryaKumar\Desktop\Hack2

# Initialize git repository
git init

# Check git status
git status
```

**Output should show**:
```
Initialized empty Git repository in C:/Users/SuryaKumar/Desktop/Hack2/.git/
```

---

## Step 3: Configure Git (First Time Only)

Set your identity:

```bash
# Set your name
git config --global user.name "Your Name"

# Set your email (use GitHub email)
git config --global user.email "your.email@example.com"

# Verify settings
git config --list
```

---

## Step 4: Review Files to Commit

**Check what will be committed**:

```bash
git status
```

**Expected output** (files in green):
```
Untracked files:
  .gitignore
  LICENSE
  PROJECT_STRUCTURE.md
  QUICKSTART.md
  README.md
  docs/
  fda_connector/
  streamlit_app/
```

**Files that will be IGNORED** (thanks to .gitignore):
```
❌ *.json (service account keys) - PROTECTED
❌ .env files - PROTECTED
❌ __pycache__/ - Not needed
❌ venv/ - Not needed
✅ configuration.json - INCLUDED (not sensitive)
```

**Important**: The .gitignore file is already configured to protect sensitive files!

---

## Step 5: Add Files to Git

```bash
# Add all files (respects .gitignore)
git add .

# Or add specific directories
git add fda_connector/
git add streamlit_app/
git add docs/
git add *.md
git add LICENSE

# Verify what's staged
git status
```

**Should show**:
```
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   .gitignore
        new file:   LICENSE
        new file:   README.md
        ... (all your files)
```

---

## Step 6: Commit Changes

```bash
# Commit with descriptive message
git commit -m "Initial commit: FDA Intelligence Dashboard

- Custom Fivetran connector for FDA data
- Streamlit dashboard with Vertex AI integration
- Complete documentation and setup guides
- Built for Fivetran × Google Cloud Challenge 2024"

# Verify commit
git log --oneline
```

---

## Step 7: Connect to GitHub

```bash
# Add remote repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/fda-intelligence-dashboard.git

# Verify remote
git remote -v
```

**Should show**:
```
origin  https://github.com/YOUR_USERNAME/fda-intelligence-dashboard.git (fetch)
origin  https://github.com/YOUR_USERNAME/fda-intelligence-dashboard.git (push)
```

---

## Step 8: Push to GitHub

```bash
# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**If prompted for credentials**:
- **Username**: Your GitHub username
- **Password**: Use a Personal Access Token (not your password!)

### Create Personal Access Token (if needed)

1. Go to: https://github.com/settings/tokens
2. Click: "Generate new token" → "Generate new token (classic)"
3. **Note**: "FDA Dashboard Token"
4. **Expiration**: 90 days
5. **Scopes**: Check `repo` (full control)
6. Click: "Generate token"
7. **Copy token** (you won't see it again!)
8. **Use as password** when pushing

---

## Step 9: Verify on GitHub

1. Go to: `https://github.com/YOUR_USERNAME/fda-intelligence-dashboard`
2. **Should see**:
   - All your files
   - README.md displayed on home page
   - MIT License badge (in "About" section)
   - Folders: `fda_connector/`, `streamlit_app/`, `docs/`

---

## Step 10: Add License Badge

GitHub should automatically detect the MIT License. To verify:

1. **Repository page** → Click "About" (gear icon)
2. **License**: Should show "MIT License"
3. If not, click "Edit" → Select "MIT License"

---

## Future Updates

### Adding New Changes

```bash
# Check what changed
git status

# Add changed files
git add .

# Commit with message
git commit -m "Add: Feature description"

# Push to GitHub
git push
```

### Common Commands

```bash
# View status
git status

# View commit history
git log --oneline

# View differences
git diff

# Undo unstaged changes
git restore <file>

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

---

## Troubleshooting

### Issue: "fatal: not a git repository"

**Solution**: Make sure you're in the correct directory
```bash
cd C:\Users\SuryaKumar\Desktop\Hack2
git init
```

### Issue: "remote origin already exists"

**Solution**: Remove and re-add
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/fda-intelligence-dashboard.git
```

### Issue: "failed to push some refs"

**Solution**: Pull first, then push
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Issue: Authentication failed

**Solution**: Use Personal Access Token
1. Create token at: https://github.com/settings/tokens
2. Use token as password when prompted

### Issue: Large files rejected

**Solution**: Check file size
```bash
# Find large files
powershell "Get-ChildItem -Recurse | Where-Object {$_.Length -gt 50MB} | Select-Object FullName, Length"
```

GitHub has a 100MB file size limit. Use Git LFS for larger files.

---

## Making Repository Look Professional

### 1. Add Topics

On GitHub repository page:
1. Click "About" (gear icon)
2. Add topics:
   - `fivetran`
   - `google-cloud`
   - `bigquery`
   - `vertex-ai`
   - `streamlit`
   - `healthcare`
   - `fda-data`
   - `hackathon`

### 2. Add Description

In "About" section:
```
AI-powered FDA data insights using Fivetran, BigQuery & Vertex AI. Built for the Fivetran × Google Cloud Challenge 2024.
```

### 3. Add Website

Add your deployed dashboard URL (Cloud Run or Streamlit Cloud)

### 4. Add Screenshots

```bash
# Create screenshots folder
mkdir screenshots

# Add your screenshots
# Then commit and push
git add screenshots/
git commit -m "Add: Dashboard screenshots"
git push
```

---

## Repository Structure (After Push)

Your GitHub repo will show:

```
fda-intelligence-dashboard/
├── 📄 README.md                    ← Displayed on homepage
├── 📄 LICENSE                      ← Visible in "About"
├── 📄 .gitignore                   ← Protects secrets
├── 📁 fda_connector/
├── 📁 streamlit_app/
├── 📁 docs/
└── 📁 screenshots/ (add these)
```

---

## GitHub Pages (Optional)

To create a project website:

1. Go to: Repository Settings → Pages
2. Source: Deploy from branch
3. Branch: main / docs
4. Save

Your documentation will be available at:
`https://YOUR_USERNAME.github.io/fda-intelligence-dashboard/`

---

## Best Practices

✅ **DO**:
- Write clear commit messages
- Commit frequently (logical chunks)
- Keep repository clean
- Update documentation
- Add meaningful README

❌ **DON'T**:
- Commit sensitive data (API keys, credentials)
- Commit large binary files
- Push directly to main (in team projects)
- Include generated files (__pycache__, etc.)

---

## Security Checklist

Before pushing, verify:

- [ ] No `*.json` service account keys (except configuration.json)
- [ ] No `.env` files
- [ ] No API keys in code
- [ ] No passwords
- [ ] .gitignore is working

**Test**:
```bash
# Check what will be committed
git status

# Search for potential secrets
git grep -i "api_key"
git grep -i "password"
git grep -i "secret"
```

If any secrets found, remove them before pushing!

---

## Next Steps After Push

1. ✅ Verify repository is public
2. ✅ Check all files are visible
3. ✅ Add topics and description
4. ✅ Add screenshots
5. ✅ Test cloning from another location
6. ✅ Share link with team/judges
7. ✅ Add to Devpost submission

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `git status` | Check current state |
| `git add .` | Stage all changes |
| `git commit -m "msg"` | Commit changes |
| `git push` | Push to GitHub |
| `git pull` | Pull from GitHub |
| `git log` | View history |
| `git diff` | View changes |

---

## Support

**Git Help**:
- Official docs: https://git-scm.com/doc
- GitHub guides: https://guides.github.com/
- GitHub docs: https://docs.github.com/

**Need help?**
- Git command help: `git <command> --help`
- GitHub community: https://github.community/

---

**You're ready to push to GitHub! 🚀**


