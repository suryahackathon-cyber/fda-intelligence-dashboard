# FDA Intelligence Dashboard 💊

> **AI-Powered FDA Data Insights using Fivetran, Google Cloud BigQuery & Vertex AI**

An intelligent healthcare data platform that syncs FDA drug safety data through a custom Fivetran connector, stores it in BigQuery, and provides AI-powered insights using Google Vertex AI Gemini.

Built for the **Fivetran × Google Cloud Challenge 2024**.

---

## 🎯 Project Overview

The FDA Intelligence Dashboard transforms how healthcare professionals and patients access critical drug safety information by:

- **Automating Data Ingestion**: Custom Fivetran connector syncs FDA adverse events, recalls, and drug labels
- **Enabling AI Analysis**: Google Vertex AI Gemini provides natural language insights and safety recommendations
- **Visualizing Trends**: Interactive Streamlit dashboard with real-time analytics
- **Democratizing Access**: Making FDA data accessible and actionable for everyone

### Problem Statement

Healthcare providers struggle to stay updated on drug safety issues. FDA data is scattered, technical, and difficult to analyze at scale. Our solution makes this data accessible, actionable, and intelligent.

---

## ✨ Features

### 🔌 Custom Fivetran Connector
- Syncs 5+ FDA datasets (adverse events, recalls, labels)
- Production-ready with error handling and rate limiting
- Configurable sync frequency and date ranges
- Automatic schema management

### 📊 Interactive Dashboard
- **Overview**: Real-time metrics and trend analysis
- **Adverse Events**: Top drugs by safety events, severity analysis
- **Recalls**: Recent recalls by classification and company
- **AI Insights**: Natural language Q&A powered by Gemini

### 🤖 AI-Powered Intelligence
- Drug safety risk assessment
- Natural language question answering
- Automated pattern detection
- Healthcare provider recommendations

---

## 🏗️ Architecture

```
┌─────────────────┐
│  FDA openFDA    │
│      API        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Fivetran     │
│   Connector     │◄─── Custom Python SDK
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   BigQuery      │
│  (Data Warehouse)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│   Streamlit     │─────►│  Vertex AI   │
│   Dashboard     │      │   Gemini     │
└─────────────────┘      └──────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Google Cloud Platform account ([Setup Guide](docs/GCP_SETUP.md))
- Fivetran account ([Free Trial](https://fivetran.com/signup))
- FDA API key ([Get Key](https://open.fda.gov/apis/authentication/))

### Installation

1. **Clone Repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/fda-intelligence-dashboard.git
   cd fda-intelligence-dashboard
   ```

2. **Deploy Fivetran Connector**:
   ```bash
   cd fda_connector
   pip install -r requirements.txt
   
   # Test locally
   python test_connector.py
   
   # Deploy to Fivetran
   fivetran connector deploy \
     --name "FDA-Data-Connector" \
     --connector-file connector.py \
     --config-file configuration.json \
     --requirements requirements.txt
   ```

3. **Setup Google Cloud** ([Detailed Guide](docs/GCP_SETUP.md)):
   ```bash
   # Enable APIs
   gcloud services enable bigquery.googleapis.com aiplatform.googleapis.com
   
   # Create dataset
   bq mk --dataset --location=US YOUR_PROJECT_ID:fda_data
   
   # Set environment variables
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
   export GCP_PROJECT_ID="your-project-id"
   export BQ_DATASET_ID="fda_data"
   ```

4. **Run Dashboard**:
   ```bash
   cd streamlit_app
   pip install -r requirements.txt
   streamlit run app.py
   ```

5. **Access Dashboard**:
   - Open browser to: `http://localhost:8501`
   - Configure GCP connection in sidebar
   - Start exploring data!

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [GCP Setup Guide](docs/GCP_SETUP.md) | Complete guide for Google Cloud Platform setup |
| [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) | Step-by-step deployment instructions |
| [Connector README](fda_connector/README.md) | Fivetran connector documentation |
| [Dashboard README](streamlit_app/README.md) | Streamlit dashboard documentation |

---

## 🎥 Demo

**Watch the 3-minute demo**: [YouTube Link](#)

### Screenshots

#### Dashboard Overview
![Dashboard Overview](screenshots/dashboard-overview.png)

#### Adverse Events Analysis
![Adverse Events](screenshots/adverse-events.png)

#### AI-Powered Insights
![AI Insights](screenshots/ai-insights.png)

---

## 🛠️ Technologies Used

### Data Pipeline
- **Fivetran Connector SDK**: Custom Python connector for FDA data
- **Google Cloud BigQuery**: Scalable data warehouse
- **openFDA API**: Official FDA data source

### AI & Analytics
- **Google Vertex AI**: Generative AI platform
- **Gemini 1.5 Flash**: Large language model for insights
- **Plotly**: Interactive visualizations

### Application
- **Streamlit**: Python web framework
- **Pandas**: Data manipulation
- **Google Cloud Run**: Serverless deployment

---

## 📊 Data Sources

The connector syncs data from these FDA endpoints:

| Endpoint | Description | Update Frequency |
|----------|-------------|------------------|
| Drug Adverse Events | Reports of adverse reactions to drugs | Daily |
| Drug Labels | Official drug labeling information | Weekly |
| Drug Recalls | Drug product recalls | Daily |
| Food Recalls | Food product recalls | Daily |
| Device Adverse Events | Medical device adverse events | Daily |

All data sourced from [openFDA](https://open.fda.gov/).

---

## 💡 Use Cases

### For Healthcare Providers
- Monitor drug safety profiles in real-time
- Get AI-powered recommendations for patient care
- Track emerging safety trends
- Access comprehensive recall information

### For Patients
- Research drug safety before starting medication
- Stay informed about drug recalls
- Understand adverse event patterns
- Make informed healthcare decisions

### For Researchers
- Analyze large-scale adverse event data
- Identify safety signals and patterns
- Export data for further analysis
- Track temporal trends

---

## 🔒 Security & Privacy

- Service account authentication with least privilege
- No patient identifiable information (PII) stored
- All data sourced from public FDA databases
- Secure credential management
- HTTPS encryption for all communications

---

## 💰 Cost Estimate

**Fivetran**:
- 14-day free trial
- ~$50-100/month after trial

**Google Cloud** (with free tier):
- BigQuery: ~$0-5/month
- Vertex AI: ~$0-2/month
- Cloud Run: ~$0-5/month
- **Total**: ~$0-12/month (within free tier limits)

---

## 🏆 Challenge Requirements Met

✅ **Custom Connector**: Built with Fivetran Connector SDK  
✅ **Google Cloud Destination**: Data syncs to BigQuery  
✅ **Google Cloud AI**: Integrated with Vertex AI Gemini  
✅ **Modern AI/Data Solution**: RAG-based Q&A and agentic insights  
✅ **Production Ready**: Error handling, logging, deployment guide  
✅ **Open Source**: MIT License  

---

## 🚧 Roadmap

### Phase 1 (Current)
- [x] FDA adverse events connector
- [x] BigQuery integration
- [x] Streamlit dashboard
- [x] Vertex AI integration

### Phase 2 (Future)
- [ ] Add predictive analytics
- [ ] Real-time alerting system
- [ ] Mobile app
- [ ] Multi-language support
- [ ] Additional FDA endpoints

### Phase 3 (Future)
- [ ] Integration with EHR systems
- [ ] Advanced ML models for safety prediction
- [ ] Comparative drug analysis
- [ ] Provider collaboration features

---

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

Built by [Your Name] for the Fivetran × Google Cloud Challenge 2024.

---

## 🙏 Acknowledgments

- **Fivetran** for the Connector SDK and challenge opportunity
- **Google Cloud** for credits and Vertex AI platform
- **FDA** for maintaining open public health data
- **Streamlit** for the amazing framework

---

## 📞 Contact & Support

- **GitHub Issues**: [Create an issue](https://github.com/YOUR_USERNAME/fda-intelligence-dashboard/issues)
- **Email**: your.email@example.com
- **Twitter**: [@YourHandle](https://twitter.com/YourHandle)

---

## 📚 Resources

- [openFDA API Documentation](https://open.fda.gov/apis/)
- [Fivetran Connector SDK Docs](https://fivetran.com/docs/connectors/connector-sdk)
- [Google Cloud BigQuery](https://cloud.google.com/bigquery/docs)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

<div align="center">

**Built with ❤️ for better healthcare outcomes**

[![Fivetran](https://img.shields.io/badge/Powered%20by-Fivetran-00A8E1?style=for-the-badge)](https://fivetran.com)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

</div>


