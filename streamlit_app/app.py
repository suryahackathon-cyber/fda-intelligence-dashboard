"""
FDA Data Intelligence Dashboard

A Streamlit dashboard that uses FDA data from Fivetran + BigQuery
and leverages Google Cloud AI (Vertex AI) for intelligent insights.
"""

import streamlit as st
import pandas as pd
from google.cloud import bigquery
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

# Page configuration
st.set_page_config(
    page_title="FDA Intelligence Dashboard",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


class FDADashboard:
    """Main dashboard class"""
    
    def __init__(self):
        """Initialize dashboard with Google Cloud connections"""
        self.bq_client = None
        self.vertex_model = None
        self.project_id = None
        self.dataset_id = None
        
    def setup_google_cloud(self, project_id: str, dataset_id: str, location: str = "us-central1"):
        """
        Setup Google Cloud connections
        
        Args:
            project_id: GCP project ID
            dataset_id: BigQuery dataset ID
            location: GCP region
        """
        try:
            # Initialize BigQuery client
            self.bq_client = bigquery.Client(project=project_id)
            self.project_id = project_id
            self.dataset_id = dataset_id
            
            # Initialize Vertex AI
            vertexai.init(project=project_id, location=location)
            self.vertex_model = GenerativeModel("gemini-1.5-flash")
            
            st.success("✅ Connected to Google Cloud successfully!")
            return True
            
        except Exception as e:
            st.error(f"❌ Error connecting to Google Cloud: {str(e)}")
            return False
    
    def query_bigquery(self, query: str) -> pd.DataFrame:
        """
        Execute BigQuery query
        
        Args:
            query: SQL query string
            
        Returns:
            DataFrame with results
        """
        try:
            df = self.bq_client.query(query).to_dataframe()
            return df
        except Exception as e:
            st.error(f"Error querying BigQuery: {str(e)}")
            return pd.DataFrame()
    
    def get_adverse_events_summary(self, table_name: str = "fda_drug_adverse_events") -> pd.DataFrame:
        """Get summary of drug adverse events"""
        query = f"""
        SELECT 
            COUNT(*) as total_events,
            COUNT(DISTINCT safetyreportid) as unique_reports,
            COUNTIF(serious = '1') as serious_events,
            COUNTIF(serious_death = '1') as deaths,
            COUNTIF(serious_hospitalization = '1') as hospitalizations
        FROM `{self.project_id}.{self.dataset_id}.{table_name}`
        """
        return self.query_bigquery(query)
    
    def get_top_drugs_by_events(self, table_name: str = "fda_drug_adverse_events", limit: int = 10) -> pd.DataFrame:
        """Get drugs with most adverse events"""
        query = f"""
        WITH drug_events AS (
            SELECT 
                REGEXP_EXTRACT(drug_names, r"'([^']+)'") as drug_name,
                safetyreportid,
                serious
            FROM `{self.project_id}.{self.dataset_id}.{table_name}`
            WHERE drug_names != '[]'
        )
        SELECT 
            drug_name,
            COUNT(*) as event_count,
            COUNTIF(serious = '1') as serious_count
        FROM drug_events
        WHERE drug_name IS NOT NULL AND drug_name != ''
        GROUP BY drug_name
        ORDER BY event_count DESC
        LIMIT {limit}
        """
        return self.query_bigquery(query)
    
    def get_events_by_date(self, table_name: str = "fda_drug_adverse_events") -> pd.DataFrame:
        """Get events timeline"""
        query = f"""
        SELECT 
            PARSE_DATE('%Y%m%d', receivedate) as event_date,
            COUNT(*) as event_count,
            COUNTIF(serious = '1') as serious_count
        FROM `{self.project_id}.{self.dataset_id}.{table_name}`
        WHERE LENGTH(receivedate) = 8 AND receivedate != ''
        GROUP BY event_date
        ORDER BY event_date DESC
        LIMIT 365
        """
        return self.query_bigquery(query)
    
    def get_recalls_summary(self, table_name: str = "fda_drug_recalls") -> pd.DataFrame:
        """Get recalls summary"""
        query = f"""
        SELECT 
            classification,
            COUNT(*) as recall_count,
            COUNT(DISTINCT company_name) as companies_affected
        FROM `{self.project_id}.{self.dataset_id}.{table_name}`
        WHERE classification IS NOT NULL
        GROUP BY classification
        ORDER BY recall_count DESC
        """
        return self.query_bigquery(query)
    
    def get_recent_recalls(self, table_name: str = "fda_drug_recalls", limit: int = 10) -> pd.DataFrame:
        """Get recent recalls"""
        query = f"""
        SELECT 
            recall_number,
            report_date,
            product_description,
            reason_for_recall,
            company_name,
            classification,
            status
        FROM `{self.project_id}.{self.dataset_id}.{table_name}`
        ORDER BY report_date DESC
        LIMIT {limit}
        """
        return self.query_bigquery(query)
    
    def analyze_with_gemini(self, data_summary: str, question: str) -> str:
        """
        Use Vertex AI Gemini to analyze data and answer questions
        
        Args:
            data_summary: Summary of the data
            question: User's question
            
        Returns:
            AI-generated insight
        """
        try:
            prompt = f"""
You are an FDA data analyst with expertise in drug safety and public health.

Data Summary:
{data_summary}

User Question: {question}

Provide a detailed, actionable insight based on the data. Include:
1. Key findings
2. Potential concerns or trends
3. Recommendations for healthcare providers or patients
4. Any patterns that warrant further investigation

Keep your response professional, data-driven, and focused on public health impact.
"""
            
            response = self.vertex_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Error generating AI insight: {str(e)}"
    
    def get_ai_safety_recommendations(self, drug_name: str, adverse_events: pd.DataFrame) -> str:
        """Get AI-powered safety recommendations for a drug"""
        
        events_summary = adverse_events.to_string() if not adverse_events.empty else "No data available"
        
        prompt = f"""
Analyze the adverse event data for {drug_name}:

{events_summary}

Provide:
1. Risk assessment summary
2. Most concerning adverse events
3. Patient populations who should be cautious
4. Recommendations for healthcare providers
5. Suggested monitoring parameters

Be concise but thorough.
"""
        
        try:
            response = self.vertex_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"


def main():
    """Main application"""
    
    # Header
    st.markdown('<h1 class="main-header">💊 FDA Intelligence Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("**Powered by Fivetran, Google Cloud BigQuery & Vertex AI**")
    st.markdown("---")
    
    # Initialize dashboard
    dashboard = FDADashboard()
    
    # Sidebar configuration
    st.sidebar.title("⚙️ Configuration")
    
    project_id = st.sidebar.text_input(
        "GCP Project ID",
        value=os.environ.get("GCP_PROJECT_ID", ""),
        help="Your Google Cloud Project ID"
    )
    
    dataset_id = st.sidebar.text_input(
        "BigQuery Dataset ID",
        value=os.environ.get("BQ_DATASET_ID", "fda_data"),
        help="BigQuery dataset where Fivetran syncs FDA data"
    )
    
    location = st.sidebar.selectbox(
        "GCP Region",
        ["us-central1", "us-east1", "us-west1", "europe-west1", "asia-east1"],
        help="Google Cloud region"
    )
    
    # Connect button
    if st.sidebar.button("🔌 Connect to Google Cloud", type="primary"):
        if project_id and dataset_id:
            dashboard.setup_google_cloud(project_id, dataset_id, location)
        else:
            st.sidebar.error("Please provide Project ID and Dataset ID")
    
    # Main content
    if dashboard.bq_client is None:
        st.info("👈 Please configure and connect to Google Cloud in the sidebar to begin")
        
        # Setup instructions
        st.markdown("## 🚀 Quick Start")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 1️⃣ Setup Fivetran Connector
            - Deploy FDA connector to Fivetran
            - Connect to BigQuery destination
            - Start syncing FDA data
            """)
        
        with col2:
            st.markdown("""
            ### 2️⃣ Configure Dashboard
            - Enter GCP Project ID
            - Specify BigQuery dataset
            - Click Connect
            """)
        
        return
    
    # Dashboard tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview",
        "⚠️ Adverse Events",
        "🔄 Recalls",
        "🤖 AI Insights"
    ])
    
    # Tab 1: Overview
    with tab1:
        st.header("Dashboard Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Get summary data
        summary = dashboard.get_adverse_events_summary()
        
        if not summary.empty:
            with col1:
                st.metric(
                    "Total Events",
                    f"{summary['total_events'].iloc[0]:,}"
                )
            
            with col2:
                st.metric(
                    "Serious Events",
                    f"{summary['serious_events'].iloc[0]:,}",
                    delta=f"{(summary['serious_events'].iloc[0] / summary['total_events'].iloc[0] * 100):.1f}%"
                )
            
            with col3:
                st.metric(
                    "Deaths Reported",
                    f"{summary['deaths'].iloc[0]:,}"
                )
            
            with col4:
                st.metric(
                    "Hospitalizations",
                    f"{summary['hospitalizations'].iloc[0]:,}"
                )
        
        st.markdown("---")
        
        # Timeline
        st.subheader("📈 Events Timeline")
        events_timeline = dashboard.get_events_by_date()
        
        if not events_timeline.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=events_timeline['event_date'],
                y=events_timeline['event_count'],
                name='All Events',
                line=dict(color='#1f77b4', width=2)
            ))
            fig.add_trace(go.Scatter(
                x=events_timeline['event_date'],
                y=events_timeline['serious_count'],
                name='Serious Events',
                line=dict(color='#ff7f0e', width=2)
            ))
            fig.update_layout(
                title='Adverse Events Over Time',
                xaxis_title='Date',
                yaxis_title='Number of Events',
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 2: Adverse Events
    with tab2:
        st.header("⚠️ Adverse Events Analysis")
        
        # Top drugs
        st.subheader("Top Drugs by Adverse Events")
        top_drugs = dashboard.get_top_drugs_by_events(limit=15)
        
        if not top_drugs.empty:
            fig = px.bar(
                top_drugs,
                x='event_count',
                y='drug_name',
                orientation='h',
                color='serious_count',
                title='Drugs with Most Reported Adverse Events',
                labels={'event_count': 'Total Events', 'drug_name': 'Drug Name', 'serious_count': 'Serious Events'},
                color_continuous_scale='Reds'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Data table
            st.subheader("Detailed Data")
            st.dataframe(top_drugs, use_container_width=True)
    
    # Tab 3: Recalls
    with tab3:
        st.header("🔄 Drug Recalls")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Recalls by Classification")
            recalls_summary = dashboard.get_recalls_summary()
            
            if not recalls_summary.empty:
                fig = px.pie(
                    recalls_summary,
                    values='recall_count',
                    names='classification',
                    title='Recall Distribution',
                    color_discrete_sequence=px.colors.sequential.RdBu
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Recent Recalls")
            recent_recalls = dashboard.get_recent_recalls()
            
            if not recent_recalls.empty:
                for _, recall in recent_recalls.iterrows():
                    with st.expander(f"🔴 {recall['product_description'][:100]}..."):
                        st.markdown(f"""
                        **Recall Number:** {recall['recall_number']}  
                        **Date:** {recall['report_date']}  
                        **Company:** {recall['company_name']}  
                        **Classification:** {recall['classification']}  
                        **Status:** {recall['status']}  
                        **Reason:** {recall['reason_for_recall']}
                        """)
    
    # Tab 4: AI Insights
    with tab4:
        st.header("🤖 AI-Powered Insights")
        st.markdown("*Powered by Google Vertex AI Gemini*")
        
        # Question answering
        st.subheader("Ask Questions About FDA Data")
        
        user_question = st.text_input(
            "What would you like to know?",
            placeholder="e.g., What are the most concerning drug safety trends?"
        )
        
        if st.button("🔍 Get AI Insight", type="primary"):
            if user_question:
                with st.spinner("Analyzing data with AI..."):
                    # Get relevant data
                    summary = dashboard.get_adverse_events_summary()
                    top_drugs = dashboard.get_top_drugs_by_events()
                    
                    data_summary = f"""
                    Total Events: {summary['total_events'].iloc[0] if not summary.empty else 0}
                    Serious Events: {summary['serious_events'].iloc[0] if not summary.empty else 0}
                    Deaths: {summary['deaths'].iloc[0] if not summary.empty else 0}
                    
                    Top Drugs by Events:
                    {top_drugs.to_string() if not top_drugs.empty else 'No data'}
                    """
                    
                    insight = dashboard.analyze_with_gemini(data_summary, user_question)
                    
                    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                    st.markdown("### 💡 AI Insight")
                    st.markdown(insight)
                    st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Drug-specific analysis
        st.subheader("Drug Safety Analysis")
        
        drug_name = st.text_input("Enter drug name for detailed analysis")
        
        if st.button("📊 Analyze Drug", type="secondary"):
            if drug_name:
                with st.spinner(f"Analyzing {drug_name}..."):
                    # Query specific drug data
                    query = f"""
                    SELECT 
                        reactions,
                        serious,
                        serious_death,
                        serious_hospitalization,
                        patient_sex,
                        patient_age
                    FROM `{dashboard.project_id}.{dashboard.dataset_id}.fda_drug_adverse_events`
                    WHERE LOWER(drug_names) LIKE LOWER('%{drug_name}%')
                    LIMIT 100
                    """
                    
                    drug_data = dashboard.query_bigquery(query)
                    
                    if not drug_data.empty:
                        recommendations = dashboard.get_ai_safety_recommendations(drug_name, drug_data)
                        
                        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                        st.markdown(f"### ⚠️ Safety Analysis: {drug_name}")
                        st.markdown(recommendations)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.warning(f"No data found for {drug_name}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built for the Fivetran × Google Cloud Challenge 2024</p>
        <p>Data source: openFDA | Powered by Fivetran, BigQuery & Vertex AI</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()


