# FDA Intelligence Dashboard

> Comprehensive Drug Safety Analytics Platform powered by Google Cloud

![Version](https://img.shields.io/badge/version-2.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Tab Descriptions](#tab-descriptions)
- [Data Model](#data-model)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The **FDA Intelligence Dashboard** is a production-ready Streamlit application that provides comprehensive analytics and visualization of FDA adverse drug event data. Built on Google Cloud Platform, it enables pharmaceutical companies, researchers, and healthcare professionals to monitor drug safety signals and conduct in-depth adverse event analysis.

### Key Capabilities

- **Real-time Analytics** - Query and visualize millions of adverse event records
- **Multi-language Support** - Translate reports into 15+ languages
- **Voice Interface** - Speech-to-text and text-to-speech capabilities
- **Interactive Visualizations** - Plotly-powered charts and graphs
- **Data Exploration** - Browse available drugs and reactions
- **Drug Safety Profiling** - Comprehensive drug-specific analysis

---

## ✨ Features

### 📊 Overview Dashboard
- **Key Metrics Cards**: Total events, serious events, deaths, hospitalizations, serious rate
- **Trend Analysis**: Time-series visualization of adverse events over 180 days
- **Top 20 Drugs**: Horizontal bar chart with serious event percentage heatmap
- **Top 20 Reactions**: Interactive treemap visualization
- **Demographics**: Age group and gender distribution
- **Severity Breakdown**: Events categorized by severity level

### 🔍 Data Explorer
- **Table Statistics**: Total rows, unique reports, date ranges
- **Available Drugs**: Top 50 drugs with event counts (searchable & copyable)
- **Available Reactions**: Top 50 reactions with counts (searchable & copyable)
- **Sample Data Preview**: View actual database structure
- **Quick Reference**: Helps users understand what data is available

### 🔎 Advanced Search
- **Keyword Search**: Search by drug name, symptom, or reaction
- **Quick Suggestions**: Clickable buttons for popular searches
- **Configurable Limits**: Return 10-200 results
- **Summary Statistics**: Aggregated metrics for search results
- **CSV Export**: Download search results

### 💊 Drug Analysis
- **Comprehensive Safety Profile**: Complete drug-specific analytics
- **5 Key Metrics**: Events, serious events, deaths, hospitalizations, serious rate
- **Top 10 Reactions**: Bar chart of most common adverse reactions
- **90-Day Trends**: Time-series of recent events
- **Demographics**: Patient distribution by gender
- **Risk Assessment**: Automated safety classification (High/Moderate/Lower risk)

### 🌐 Translation
- **15 Languages Supported**:
  - Spanish (🇪🇸), French (🇫🇷), German (🇩🇪)
  - Chinese (🇨🇳), Japanese (🇯🇵), Korean (🇰🇷)
  - Hindi (🇮🇳), Arabic (🇸🇦), Portuguese (🇵🇹)
  - Russian (🇷🇺), Italian (🇮🇹), Dutch (🇳🇱)
  - Polish (🇵🇱), Turkish (🇹🇷), Vietnamese (🇻🇳)
- **Real-time Translation**: Instant text translation
- **Copy Support**: Easy copy-to-clipboard functionality

### 🎤 Voice Interface
- **Speech-to-Text**: Transcribe WAV audio files to text
- **Text-to-Speech**: Generate MP3 audio from text
- **Audio Player**: In-browser audio playback
- **Download Support**: Save generated audio files

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                        │
│  (Interactive UI with Tabs, Charts, Forms)                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  FDADashboard Class                          │
│  (Business Logic & Data Processing)                         │
└─────┬──────────┬──────────┬──────────┬──────────┬──────────┘
      │          │          │          │          │
      ▼          ▼          ▼          ▼          ▼
┌──────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│BigQuery  │ │Transla-│ │Speech  │ │Text-to-│ │Data    │
│Analytics │ │tion API│ │to-Text │ │Speech  │ │Storage │
└──────────┘ └────────┘ └────────┘ └────────┘ └────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│           BigQuery Dataset: fda_data                         │
│   Table: fda_drug_adverse_events                            │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│              FDA openFDA API                                 │
│   (Source: https://open.fda.gov)                            │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit 1.28+ | Interactive web interface |
| **Visualization** | Plotly 5.17+ | Interactive charts and graphs |
| **Database** | Google BigQuery | Data warehouse and analytics |
| **Translation** | Google Cloud Translation API | Multi-language support |
| **Speech** | Google Cloud Speech APIs | Voice interface |
| **Data Processing** | Pandas 2.0+ | Data manipulation |
| **Language** | Python 3.8+ | Application logic |

---

## 📋 Prerequisites

### Required
- **Google Cloud Platform Account**
- **GCP Project** with billing enabled
- **BigQuery Dataset** with FDA data
- **Python 3.8 or higher**

### Google Cloud APIs (Must be enabled)
```bash
gcloud services enable bigquery.googleapis.com
gcloud services enable translate.googleapis.com
gcloud services enable speech.googleapis.com
gcloud services enable texttospeech.googleapis.com
```

### Service Account Permissions
Your service account needs these roles:
- `roles/bigquery.admin`
- `roles/serviceusage.serviceUsageConsumer`
- `roles/cloudtranslate.user` (optional)
- `roles/speech.admin` (optional)
- `roles/texttospeech.admin` (optional)

---

## 🚀 Installation

### Step 1: Clone or Download

```bash
# Create project directory
mkdir fda-intelligence-dashboard
cd fda-intelligence-dashboard

# Create app file
touch app_final_v2.py
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```txt
streamlit>=1.28.0
pandas>=2.0.0
google-cloud-bigquery>=3.11.0
google-cloud-translate>=3.12.0
google-cloud-speech>=2.21.0
google-cloud-texttospeech>=2.14.0
plotly>=5.17.0
```

### Step 3: Set Up Authentication

**Option A: Application Default Credentials (Recommended for Cloud Shell)**
```bash
gcloud auth application-default login
```

**Option B: Service Account Key**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

### Step 4: Grant Service Account Permissions

```bash
PROJECT_ID="your-project-id"
SERVICE_ACCOUNT="your-service-account@project.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/bigquery.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/serviceusage.serviceUsageConsumer"
```

---

## ⚙️ Configuration

### Environment Variables

```bash
# Required
export GCP_PROJECT="your-project-id"
export BQ_DATASET="fda_data"

# Optional (if not using default credentials)
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
```

### In-App Configuration

When you launch the app, configure in the sidebar:

1. **GCP Project ID**: Your Google Cloud project ID
2. **BigQuery Dataset**: Name of your BigQuery dataset (default: `fda_data`)
3. Click **"🔗 Connect to Google Cloud"**

---

## 🎮 Usage

### Starting the Application

```bash
streamlit run app_final_v2.py --server.port 8501
```

### Accessing the Dashboard

**Local Development:**
```
http://localhost:8501
```

**Cloud Shell:**
1. Click "Web Preview" button
2. Select "Preview on port 8501"

### Quick Start Guide

#### 1. Connect to Google Cloud
- Enter your Project ID and Dataset ID in the sidebar
- Click "Connect to Google Cloud"
- Wait for all services to initialize

#### 2. Explore Available Data
- Navigate to **"🔍 Data Explorer"** tab
- Review available drugs and reactions
- Copy drug/reaction names for searching

#### 3. View Overview
- Go to **"📊 Overview"** tab
- View key metrics and trends
- Explore top drugs and reactions

#### 4. Search for Events
- Navigate to **"🔎 Search"** tab
- Use drug/reaction names from Data Explorer
- Click quick suggestion buttons or enter custom search
- Download results as CSV

#### 5. Analyze Specific Drugs
- Go to **"💊 Drug Analysis"** tab
- Click a suggested drug or enter drug name
- Review safety profile and risk assessment

#### 6. Use Translation (Optional)
- Navigate to **"🌐 Translation"** tab
- Enter text and select target language
- Copy translated output

#### 7. Use Voice Features (Optional)
- Go to **"🎤 Voice"** tab
- Upload audio for transcription OR
- Enter text to generate speech

---

## 📑 Tab Descriptions

### 📊 Overview Dashboard

**Purpose**: High-level view of all FDA adverse event data

**Key Components**:
- **5 Metric Cards**: Gradient-styled cards showing total events, serious events, deaths, hospitalizations, and serious rate
- **Trend Chart**: Line chart with area fill showing events over last 180 days
- **Top Drugs Chart**: Horizontal bar chart with color-coded serious event percentage
- **Reactions Treemap**: Hierarchical visualization of common reactions
- **Demographics**: Age group distribution and gender breakdown

**Use Cases**:
- Executive reporting
- Trend identification
- Comparative analysis
- Safety signal detection

---

### 🔍 Data Explorer

**Purpose**: Understand what data is available in the database

**Key Components**:

1. **Table Statistics**
   - Total rows in database
   - Unique safety reports
   - Records with drug names
   - Records with reactions
   - Date range of data

2. **Top 50 Available Drugs**
   - Searchable table with drug names and event counts
   - Sorted by frequency
   - Copyable list for easy reference

3. **Top 50 Available Reactions**
   - Searchable table with reaction names and counts
   - Sorted by frequency
   - Copyable list for search queries

4. **Sample Data**
   - First 10 rows of actual data
   - Shows data structure and format
   - Helps understand field contents

**Use Cases**:
- First-time users learning the system
- Finding correct drug/reaction names
- Understanding data scope
- Planning analysis queries

---

### 🔎 Advanced Search

**Purpose**: Find specific adverse events by keyword

**Key Components**:

1. **Search Interface**
   - Text input for search term
   - Result limit selector (10-200)
   - Quick suggestion buttons for top drugs/reactions

2. **Results Display**
   - Summary statistics (total, serious, deaths, hospitalizations)
   - Full data table with all fields
   - CSV download button

3. **Search Tips**
   - Link to Data Explorer
   - Suggestions for better results
   - Common search patterns

**Search Examples**:
```
✅ Good searches:
- aspirin
- headache
- nausea
- cardiovascular

❌ Searches that won't work:
- "aspirin and headache" (use single terms)
- Misspelled drug names
- Terms not in the database
```

**Use Cases**:
- Case investigation
- Pattern identification
- Export specific subsets
- Regulatory reporting

---

### 💊 Drug Analysis

**Purpose**: Comprehensive safety profile for specific drugs

**Key Components**:

1. **Drug Selection**
   - Text input for drug name
   - Quick buttons for popular drugs
   - Auto-populated from search history

2. **Safety Metrics**
   - Total events
   - Serious events count and percentage
   - Deaths
   - Hospitalizations
   - Serious rate

3. **Visualizations**
   - **Top 10 Reactions**: Horizontal bar chart
   - **90-Day Trend**: Line chart of recent events
   - **Demographics**: Gender distribution pie chart

4. **Risk Assessment**
   - **High Risk** (>50% serious): Red warning box
   - **Moderate Risk** (25-50% serious): Yellow warning box
   - **Lower Risk** (<25% serious): Green success box

**Interpretation Guide**:

| Serious Rate | Classification | Recommendation |
|--------------|----------------|----------------|
| > 50% | High Risk | Enhanced monitoring required |
| 25-50% | Moderate Risk | Standard monitoring protocols |
| < 25% | Lower Risk | Routine surveillance |

**Use Cases**:
- Drug safety surveillance
- Risk-benefit assessment
- Regulatory submissions
- Clinical decision support

---

### 🌐 Translation

**Purpose**: Translate safety information into multiple languages

**Supported Languages**:
- Spanish, French, German
- Chinese (Simplified), Japanese, Korean
- Hindi, Arabic, Portuguese
- Russian, Italian, Dutch
- Polish, Turkish, Vietnamese

**Key Components**:
- Large text area for input
- Language selector dropdown
- Translate button
- Formatted output with copy support

**Use Cases**:
- Global safety reporting
- Patient communication materials
- Regulatory submissions for international markets
- Multi-language safety labels

**Best Practices**:
- Keep text under 5,000 characters for best results
- Review translations for medical accuracy
- Use professional translation for regulatory documents

---

### 🎤 Voice Interface

**Purpose**: Accessibility features for audio interaction

**Components**:

#### 🎙️ Speech-to-Text
- **Input**: WAV audio files
- **Output**: Transcribed text
- **Use Case**: Convert verbal case reports to text

**Supported Format**:
- Format: WAV
- Encoding: LINEAR16
- Language: English (US)

#### 🔊 Text-to-Speech
- **Input**: Text (up to 5,000 characters)
- **Output**: MP3 audio file
- **Features**: In-browser playback and download

**Voice Settings**:
- Language: English (US)
- Gender: Neutral
- Format: MP3

**Use Cases**:
- Accessibility for visually impaired users
- Audio safety alerts
- Verbal case summaries
- Training materials

---

## 📊 Data Model

### BigQuery Table: `fda_drug_adverse_events`

| Column Name | Type | Description | Example |
|------------|------|-------------|---------|
| `safetyreportid` | STRING | Unique report identifier | "12345678" |
| `receivedate` | STRING | Date report received (YYYYMMDD) | "20240115" |
| `drug_names` | STRING | JSON array of drug names | "['ASPIRIN', 'IBUPROFEN']" |
| `reactions` | STRING | JSON array of reactions | "['HEADACHE', 'NAUSEA']" |
| `patient_age` | FLOAT | Patient age in years | 45.5 |
| `patient_sex` | STRING | Patient gender (1=Male, 2=Female) | "1" |
| `serious` | STRING | Serious event flag (0/1) | "1" |
| `serious_death` | STRING | Death outcome (0/1) | "0" |
| `serious_hospitalization` | STRING | Hospitalization outcome (0/1) | "1" |
| `fetched_at` | TIMESTAMP | Data ingestion timestamp | "2024-01-15 10:30:00 UTC" |

### Data Flow

```
openFDA API → Cloud Function → BigQuery → Streamlit Dashboard
```

1. **Data Ingestion**: Cloud Function pulls data from openFDA API
2. **Storage**: Data stored in BigQuery table
3. **Processing**: Streamlit queries BigQuery for analytics
4. **Visualization**: Plotly renders interactive charts

---

## 🔧 API Reference

### FDADashboard Class

#### Methods

##### `setup_services(project_id: str, dataset_id: str) -> bool`
Initialize Google Cloud services.

**Parameters:**
- `project_id`: GCP project ID
- `dataset_id`: BigQuery dataset name

**Returns:** `True` if successful, `False` otherwise

---

##### `query(sql: str) -> pd.DataFrame`
Execute BigQuery SQL query.

**Parameters:**
- `sql`: SQL query string

**Returns:** Pandas DataFrame with results

---

##### `get_overall_summary() -> pd.DataFrame`
Get summary statistics for all events.

**Returns:** DataFrame with columns:
- `total_events`
- `unique_reports`
- `serious_events`
- `deaths`
- `hospitalizations`
- `mild_events`

---

##### `get_top_drugs(limit: int = 20) -> pd.DataFrame`
Get drugs with most adverse events.

**Parameters:**
- `limit`: Number of results (default: 20)

**Returns:** DataFrame with columns:
- `drug_name`
- `event_count`
- `serious_count`
- `death_count`
- `serious_percentage`

---

##### `get_drug_analysis(drug_name: str) -> dict`
Get comprehensive analysis for specific drug.

**Parameters:**
- `drug_name`: Drug name to analyze

**Returns:** Dictionary containing:
- `stats`: Basic statistics DataFrame
- `reactions`: Top reactions DataFrame
- `demographics`: Gender distribution DataFrame
- `trends`: Time-series DataFrame

---

##### `search_events(search_term: str, limit: int = 50) -> pd.DataFrame`
Search adverse events by keyword.

**Parameters:**
- `search_term`: Keyword to search
- `limit`: Maximum results (default: 50)

**Returns:** DataFrame with matching events

---

##### `translate_text(text: str, target_lang: str) -> str`
Translate text to target language.

**Parameters:**
- `text`: Text to translate
- `target_lang`: Target language code (e.g., 'es', 'fr')

**Returns:** Translated text string

---

##### `transcribe_audio(audio_file) -> str`
Transcribe audio file to text.

**Parameters:**
- `audio_file`: Uploaded WAV file object

**Returns:** Transcribed text

---

##### `synthesize_speech(text: str) -> bytes`
Convert text to speech audio.

**Parameters:**
- `text`: Text to convert

**Returns:** MP3 audio as bytes

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Connection Error: 403 Permission Denied

**Symptom:**
```
403 Caller does not have required permission to use project
```

**Solution:**
```bash
# Grant service account permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:YOUR_SA@PROJECT.iam.gserviceaccount.com" \
  --role="roles/bigquery.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:YOUR_SA@PROJECT.iam.gserviceaccount.com" \
  --role="roles/serviceusage.serviceUsageConsumer"

# Wait 60 seconds for propagation
```

---

#### 2. No Data Returned from Search

**Symptom:** Search returns 0 results

**Solutions:**
1. Check Data Explorer tab for available terms
2. Use single-word search terms
3. Check spelling
4. Verify data exists in BigQuery:
   ```bash
   bq query --use_legacy_sql=false "SELECT COUNT(*) FROM fda_data.fda_drug_adverse_events"
   ```

---

#### 3. Translation API Not Available

**Symptom:** Warning message about Translation API

**Solution:**
```bash
# Enable the API
gcloud services enable translate.googleapis.com

# Grant permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:YOUR_SA@PROJECT.iam.gserviceaccount.com" \
  --role="roles/cloudtranslate.user"
```

---

#### 4. Charts Not Displaying

**Symptom:** Empty chart areas

**Solutions:**
1. Check if query returned data
2. Verify Plotly version: `pip install plotly>=5.17.0`
3. Check browser console for JavaScript errors
4. Try different browser

---

#### 5. Slow Performance

**Symptom:** Long query times

**Solutions:**
1. Reduce result limits
2. Optimize BigQuery table with partitioning:
   ```sql
   CREATE OR REPLACE TABLE fda_data.fda_drug_adverse_events
   PARTITION BY DATE(PARSE_TIMESTAMP('%Y%m%d', receivedate))
   AS SELECT * FROM fda_data.fda_drug_adverse_events
   ```
3. Use Cloud Shell closer to data region
4. Check BigQuery quotas

---

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

View Streamlit logs:
```bash
streamlit run app_final_v2.py --server.port 8501 --logger.level=debug
```

---

## 📈 Performance Optimization

### BigQuery Best Practices

1. **Use Partitioning:**
   ```sql
   CREATE TABLE fda_data.fda_drug_adverse_events_partitioned
   PARTITION BY DATE(PARSE_TIMESTAMP('%Y%m%d', receivedate))
   AS SELECT * FROM fda_data.fda_drug_adverse_events
   ```

2. **Create Indexes:**
   ```sql
   CREATE INDEX idx_drug_names ON fda_data.fda_drug_adverse_events(drug_names)
   ```

3. **Limit Query Results:**
   - Use `LIMIT` clauses
   - Filter on partitioned columns
   - Cache frequently-used queries

### Streamlit Optimization

1. **Use Caching:**
   ```python
   @st.cache_data(ttl=3600)
   def get_top_drugs():
       return dashboard.get_top_drugs()
   ```

2. **Session State:**
   ```python
   if 'data' not in st.session_state:
       st.session_state.data = load_data()
   ```

3. **Lazy Loading:**
   - Load data only when tabs are accessed
   - Use pagination for large result sets

---

## 🔒 Security Best Practices

1. **Service Account Keys:**
   - Never commit keys to version control
   - Use environment variables
   - Rotate keys regularly

2. **IAM Permissions:**
   - Follow principle of least privilege
   - Use separate service accounts for dev/prod
   - Enable audit logging

3. **Data Access:**
   - Implement row-level security in BigQuery
   - Use VPC Service Controls
   - Enable data encryption

4. **API Security:**
   - Use API keys for Translation/Speech APIs
   - Implement rate limiting
   - Monitor API usage

---

## 📝 Changelog

### Version 2.0 (Current)
- ✨ Added Data Explorer tab
- ✨ Quick suggestion buttons in search
- ✨ Enhanced drug analysis with risk assessment
- 🐛 Fixed search not returning results
- 🐛 Fixed color scheme issues
- 📚 Improved documentation
- ⚡ Performance optimizations

### Version 1.0
- 🎉 Initial release
- ✅ Overview dashboard
- ✅ Search functionality
- ✅ Drug analysis
- ✅ Translation support
- ✅ Voice interface

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone repo
git clone https://github.com/yourusername/fda-dashboard.git
cd fda-dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Run app
streamlit run app_final_v2.py
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 FDA Intelligence Dashboard

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Support

### Getting Help

- **Documentation**: Read this README thoroughly
- **Issues**: [GitHub Issues](https://github.com/yourusername/fda-dashboard/issues)
- **Email**: support@example.com
- **Slack**: [Join our Slack](https://slack.example.com)

### Useful Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [openFDA API](https://open.fda.gov/apis/)
- [Plotly Documentation](https://plotly.com/python/)

---

## 🙏 Acknowledgments

- **openFDA** - For providing public access to FDA data
- **Google Cloud Platform** - For cloud infrastructure and APIs
- **Streamlit** - For the amazing web framework
- **Plotly** - For interactive visualizations
- **Contributors** - Everyone who has contributed to this project

---

## 📊 Project Stats

- **Lines of Code**: ~800
- **Functions**: 20+
- **API Integrations**: 4
- **Supported Languages**: 15+
- **Visualizations**: 10+
- **Tabs**: 6

---

## 🗺️ Roadmap

### Planned Features

- [ ] Real-time alerting system
- [ ] Advanced filtering options
- [ ] Export to PDF reports
- [ ] User authentication
- [ ] Customizable dashboards
- [ ] Machine learning predictions
- [ ] Mobile app
- [ ] REST API
- [ ] Automated scheduled reports
- [ ] Integration with FAERS database

---

## 📸 Screenshots

### Overview Dashboard
![Overview Dashboard](screenshots/overview.png)

### Data Explorer
![Data Explorer](screenshots/explorer.png)

### Drug Analysis
![Drug Analysis](screenshots/drug-analysis.png)

### Search Results
![Search Results](screenshots/search.png)

---

**Built with ❤️ for pharmaceutical safety**

*Last Updated: October 24, 2025*
