# Project Structure

Complete overview of the FDA Intelligence Dashboard project structure.

```
fda-intelligence-dashboard/
│
├── fda_connector/                    # Custom Fivetran Connector
│   ├── connector.py                  # Main connector implementation
│   ├── configuration.json            # Connector configuration schema
│   ├── requirements.txt              # Python dependencies
│   ├── test_connector.py             # Local testing script
│   └── README.md                     # Connector documentation
│
├── streamlit_app/                    # Streamlit Dashboard
│   ├── app.py                        # Main dashboard application
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile                    # Container configuration
│   ├── env.example                   # Environment variables template
│   ├── .streamlit/                   # Streamlit configuration
│   │   └── config.toml               # UI theme and settings
│   └── README.md                     # Dashboard documentation
│
├── docs/                             # Documentation
│   ├── GCP_SETUP.md                  # Google Cloud setup guide
│   ├── DEPLOYMENT_GUIDE.md           # Complete deployment guide
│   └── FAQ.md                        # Frequently asked questions
│
├── README.md                         # Main project documentation
├── QUICKSTART.md                     # 15-minute quick start guide
├── LICENSE                           # MIT License
├── .gitignore                        # Git ignore rules
├── PROJECT_STRUCTURE.md              # This file
│
└── (To be added by you)
    ├── screenshots/                  # Dashboard screenshots
    │   ├── dashboard-overview.png
    │   ├── adverse-events.png
    │   └── ai-insights.png
    └── demo/                         # Demo materials
        └── demo-video.mp4
```

---

## File Descriptions

### Fivetran Connector (`fda_connector/`)

#### `connector.py`
**Purpose**: Main connector implementation using Fivetran Connector SDK

**Key Features**:
- Syncs 5 FDA endpoints (drug adverse events, drug labels, recalls, etc.)
- Implements incremental sync with state management
- Error handling and rate limiting
- Configurable date ranges and batch sizes
- Production-ready logging

**Main Classes**:
- `FDAConnector`: Core connector class
  - `__init__()`: Initialize with configuration
  - `schema()`: Define BigQuery table schemas
  - `update()`: Main sync method (generator pattern)
  - `_make_request()`: API calls with retry logic
  - `_extract_record_data()`: Data transformation

**Entry Points** (required by Fivetran):
- `schema(configuration)`: Schema definition
- `update(configuration, state)`: Incremental sync

**Lines of Code**: ~500

#### `configuration.json`
**Purpose**: Defines user-configurable parameters

**Configuration Options**:
```json
{
  "api_key": "FDA API key (optional)",
  "endpoint": "Which FDA dataset to sync",
  "start_date": "YYYY-MM-DD format",
  "limit_per_request": "1-1000 records"
}
```

#### `test_connector.py`
**Purpose**: Local testing without Fivetran deployment

**Usage**:
```bash
python test_connector.py
```

**Output**: Sample data fetch with schema and records

#### `requirements.txt`
**Dependencies**:
- `requests`: HTTP API calls
- `fivetran-connector-sdk`: Fivetran SDK

---

### Streamlit Dashboard (`streamlit_app/`)

#### `app.py`
**Purpose**: Interactive web dashboard with AI features

**Main Components**:

1. **FDADashboard Class**:
   - `setup_google_cloud()`: Initialize GCP connections
   - `query_bigquery()`: Execute SQL queries
   - `get_adverse_events_summary()`: Aggregate metrics
   - `get_top_drugs_by_events()`: Rankings
   - `analyze_with_gemini()`: AI insights
   - `get_ai_safety_recommendations()`: Drug analysis

2. **UI Tabs**:
   - **Overview**: Metrics, timelines, trends
   - **Adverse Events**: Drug rankings, severity analysis
   - **Recalls**: Recent recalls, classifications
   - **AI Insights**: Q&A and recommendations

3. **Visualizations**:
   - Plotly time series charts
   - Bar charts for rankings
   - Pie charts for distributions
   - Interactive data tables

**Lines of Code**: ~600

#### `Dockerfile`
**Purpose**: Containerize dashboard for Cloud Run deployment

**Base Image**: `python:3.11-slim`

**Key Steps**:
1. Install system dependencies
2. Copy and install Python packages
3. Copy application files
4. Expose port 8501
5. Health check endpoint
6. Run Streamlit

#### `.streamlit/config.toml`
**Purpose**: Streamlit UI theme and server configuration

**Settings**:
- Color scheme (blue theme)
- Server configuration
- CORS settings

---

### Documentation (`docs/`)

#### `GCP_SETUP.md`
**Purpose**: Complete Google Cloud Platform setup guide

**Sections** (15,000+ words):
1. Creating GCP account (free trial, credits)
2. Project setup
3. Enabling APIs (BigQuery, Vertex AI)
4. BigQuery dataset creation
5. Vertex AI configuration
6. Service account management
7. Fivetran destination setup
8. Cost management and budgets
9. Troubleshooting guide
10. Quick reference commands

**Target Audience**: Complete beginners to GCP

#### `DEPLOYMENT_GUIDE.md`
**Purpose**: Step-by-step deployment instructions

**Sections** (12,000+ words):
1. Prerequisites checklist
2. Deploying FDA connector
3. Configuring Fivetran → BigQuery
4. Dashboard deployment options:
   - Local development
   - Google Cloud Run
   - Streamlit Cloud
5. Testing and verification
6. Project submission guide
7. Troubleshooting

**Target Audience**: Hackathon participants

#### `FAQ.md`
**Purpose**: Common questions and answers

**Categories**:
- General questions
- Technical questions
- Setup troubleshooting
- Connector questions
- Deployment questions
- Cost questions
- Data questions
- AI questions
- Challenge-specific

**Entries**: 30+ Q&A pairs

---

### Root Files

#### `README.md`
**Purpose**: Main project documentation and showcase

**Sections**:
1. Project overview and problem statement
2. Features list
3. Architecture diagram
4. Quick start guide
5. Documentation index
6. Demo and screenshots
7. Technologies used
8. Data sources
9. Use cases
10. Security and privacy
11. Cost estimates
12. Challenge requirements
13. Roadmap
14. Contributing guidelines
15. License and acknowledgments

**Style**: Professional, comprehensive, GitHub-ready

#### `QUICKSTART.md`
**Purpose**: Get running in 15 minutes

**Approach**:
- Time-boxed sections (5 min each)
- Copy-paste commands
- Minimal explanation
- Quick verification steps

**Target**: Experienced developers who want to move fast

#### `LICENSE`
**Purpose**: Open source MIT license

**Permits**:
- Commercial use
- Modification
- Distribution
- Private use

**Conditions**:
- Include copyright notice
- Include license text

#### `.gitignore`
**Purpose**: Prevent sensitive files from being committed

**Excluded**:
- Python cache files
- Virtual environments
- Google Cloud credentials (*.json except config)
- Environment variables (.env)
- IDE files
- Logs and temporary files

---

## Technology Stack

### Data Pipeline
```
openFDA API
    ↓
Python Connector (Fivetran SDK)
    ↓
Fivetran Orchestration
    ↓
Google BigQuery
```

### Dashboard
```
BigQuery (data source)
    ↓
Python (pandas, queries)
    ↓
Streamlit (web framework)
    ↓
Plotly (visualizations)
    ↓
Vertex AI (AI insights)
```

### Infrastructure
```
Docker Container
    ↓
Google Cloud Run (or Streamlit Cloud)
    ↓
HTTPS Endpoint
```

---

## Data Flow

### Sync Flow
```
1. Fivetran triggers connector (scheduled)
2. Connector fetches from openFDA API
3. Data transformed to schema
4. Loaded to BigQuery table
5. State saved for next sync
```

### Query Flow
```
1. User opens dashboard
2. Dashboard connects to BigQuery
3. Executes SQL query
4. Results returned to pandas DataFrame
5. Visualized with Plotly
6. Displayed in Streamlit UI
```

### AI Flow
```
1. User asks question
2. Dashboard retrieves relevant data
3. Constructs prompt with data context
4. Calls Vertex AI Gemini API
5. AI generates insight
6. Displayed to user
```

---

## Key Design Decisions

### Why Fivetran SDK?
- Production-ready orchestration
- Built-in monitoring and logging
- Automatic scaling
- State management
- Challenge requirement

### Why BigQuery?
- Serverless, no management
- Excellent for analytics
- Native Vertex AI integration
- Generous free tier
- Challenge requirement

### Why Vertex AI Gemini?
- Native GCP integration
- Fast (Flash model)
- Cost-effective
- 1M token context
- Challenge requirement

### Why Streamlit?
- Rapid development
- Python-native (no HTML/CSS/JS)
- Beautiful UI out of the box
- Easy deployment options
- Great for dashboards

---

## Code Statistics

| Component | Files | Lines of Code | Documentation |
|-----------|-------|---------------|---------------|
| Connector | 3 | ~500 | 200 lines |
| Dashboard | 2 | ~600 | 150 lines |
| Documentation | 4 | N/A | 30,000+ words |
| **Total** | **9** | **~1,100** | **30,000+ words** |

---

## What to Add Next

### Before Submission

1. **Screenshots**:
   ```
   screenshots/
   ├── dashboard-overview.png      (full dashboard)
   ├── adverse-events.png          (charts and data)
   ├── ai-insights.png             (AI in action)
   ├── fivetran-connector.png      (connector setup)
   └── bigquery-data.png           (data in BigQuery)
   ```

2. **Demo Video** (3 minutes):
   - Record screen capture
   - Show: Connector → Data → Dashboard → AI
   - Upload to YouTube (public)
   - Add link to README

3. **Update README**:
   - Replace placeholder images
   - Add your GitHub username
   - Add demo video link
   - Add hosted URL

### After Submission

1. **Additional Features**:
   - More FDA endpoints
   - Advanced visualizations
   - Email alerts
   - Data export functionality
   - User authentication

2. **Improvements**:
   - Performance optimization
   - Additional AI prompts
   - Mobile responsive design
   - Automated testing
   - CI/CD pipeline

---

## File Ownership

| Component | Purpose | Owner |
|-----------|---------|-------|
| `connector.py` | Data extraction | Fivetran runtime |
| `app.py` | Web interface | Cloud Run / Streamlit Cloud |
| BigQuery tables | Data storage | Google Cloud |
| Service accounts | Authentication | Google Cloud IAM |
| API keys | FDA access | Developer |

---

## Security Considerations

### Secrets Management

**Never commit**:
- `*.json` (service account keys)
- `.env` files
- API keys in code
- Passwords

**Use instead**:
- Environment variables
- GCP Secret Manager
- Streamlit secrets.toml (for Streamlit Cloud)
- Cloud Run environment variables

### Access Control

**Service Accounts**:
- Dashboard SA: Read-only (BigQuery Viewer, Vertex AI User)
- Fivetran SA: Write access (BigQuery Editor)

**Principle of Least Privilege**: Each account has minimal permissions needed

---

## Maintenance

### Regular Tasks

**Weekly**:
- Monitor Fivetran sync status
- Check BigQuery costs
- Review dashboard errors

**Monthly**:
- Update dependencies
- Review GCP billing
- Backup configuration

**As Needed**:
- Respond to FDA API changes
- Update AI prompts
- Add new features

---

## Support Resources

| Resource | URL |
|----------|-----|
| Fivetran SDK Docs | https://fivetran.com/docs/connectors/connector-sdk |
| BigQuery Docs | https://cloud.google.com/bigquery/docs |
| Vertex AI Docs | https://cloud.google.com/vertex-ai/docs |
| Streamlit Docs | https://docs.streamlit.io |
| openFDA API | https://open.fda.gov/apis |

---

## License

MIT License - Free to use, modify, and distribute with attribution.

See [LICENSE](LICENSE) file for full text.

---

**Last Updated**: 2024
**Version**: 1.0.0
**Status**: Ready for submission ✅


