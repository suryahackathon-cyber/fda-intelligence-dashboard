cd ~/fda-intelligence-dashboard/streamlit_app

# Create an improved version with data exploration
cat > app_final_v2.py << 'EOF'
"""
FDA Intelligence Dashboard - Final Working Version v2

Added:
- Data Explorer tab showing available values
- Improved search with suggestions
- Better error handling
"""

import streamlit as st
import pandas as pd
from google.cloud import bigquery
from google.cloud import translate_v2 as translate
from google.cloud import speech_v1 as speech
from google.cloud import texttospeech
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import base64
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="FDA Intelligence Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(120deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem 0;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
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
    .success-box {
        background-color: #d4edda;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    .data-sample {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        font-family: monospace;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


class FDADashboard:
    """FDA Intelligence Dashboard"""
    
    def __init__(self):
        self.bq_client = None
        self.translate_client = None
        self.speech_client = None
        self.tts_client = None
        self.project_id = None
        self.dataset_id = None
        
    def setup_services(self, project_id: str, dataset_id: str):
        """Setup Google Cloud services"""
        try:
            self.project_id = project_id
            self.dataset_id = dataset_id
            
            # BigQuery (Required)
            self.bq_client = bigquery.Client(project=project_id)
            st.success("✅ BigQuery connected")
            
            # Translation API (Optional)
            try:
                self.translate_client = translate.Client()
                st.success("✅ Translation API connected")
            except Exception as e:
                st.warning("⚠️ Translation API not available")
                self.translate_client = None
            
            # Speech APIs (Optional)
            try:
                self.speech_client = speech.SpeechClient()
                self.tts_client = texttospeech.TextToSpeechClient()
                st.success("✅ Speech APIs connected")
            except Exception as e:
                st.warning("⚠️ Speech APIs not available")
                self.speech_client = None
                self.tts_client = None
            
            return True
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            return False
    
    def query(self, sql: str) -> pd.DataFrame:
        """Execute BigQuery query"""
        try:
            return self.bq_client.query(sql).to_dataframe()
        except Exception as e:
            st.error(f"Query error: {str(e)}")
            return pd.DataFrame()
    
    # ==================== Data Explorer ====================
    
    def get_available_drugs(self, limit: int = 50) -> pd.DataFrame:
        """Get list of available drugs"""
        query = f"""
        SELECT DISTINCT
            REGEXP_EXTRACT(drug_names, r"'([^']+)'") as drug_name,
            COUNT(*) as event_count
        FROM `{self.project_id}.{self.dataset_id}.fda_drug_adverse_events`
        WHERE drug_names IS NOT NULL AND drug_names != '[]'
        GROUP BY drug_name
        HAVING drug_name IS NOT NULL AND drug_name != ''
        ORDER BY event_count DESC
        LIMIT {limit}
        """
        return self.query(query)
    
    def get_available_reactions(self, limit: int = 50) -> pd.DataFrame:
        """Get list of available reactions"""
        query = f"""
        WITH reactions_unnested AS (
            SELECT REGEXP_EXTRACT_ALL(reactions, r"'([^']+)'") as reaction_array
            FROM `{self.project_id}.{self.dataset_id}.fda_drug_adverse_events`
            WHERE reactions IS NOT NULL AND reactions != '[]'
            LIMIT 1000
        )
        SELECT 
            reaction,
            COUNT(*) as count
        FROM reactions_unnested, UNNEST(reaction_array) as reaction
        WHERE reaction != ''
        GROUP BY reaction
        ORDER BY count DESC
        LIMIT {limit}
        """
        return self.query(query)
    
    def get_data_sample(self) -> pd.DataFrame:
        """Get sample data"""
        query = f"""
        SELECT 
            safetyreportid,
            receivedate,
            drug_names,
            reactions,
            patient_age,
            patient_sex,
            serious
        FROM `{self.project_id}.{self.dataset_id}.fda_drug_adverse_events`
        LIMIT 10
        """
        return self.query(query)
    
    def get_table_stats(self) -> dict:
        """Get table statistics"""
        stats_query = f"""
        SELECT 
            COUNT(*) as total_rows,
            COUNT(DISTINCT safetyreportid) as unique_reports,
            COUNTIF(drug_names IS NOT NULL AND drug_names != '[]') as rows_with_drugs,
            COUNTIF(reactions IS NOT NULL AND reactions != '[]') as rows_with_reactions,
            MIN(receivedate) as earliest_date,
            MAX(receivedate) as latest_date
        FROM `{self.project_id}.{self.dataset_id}.fda_drug_adverse_events`
        """
        return self.query(stats_query)
    
    # ==================== Dashboard Analytics ====================
    
    def get_overall_summary(self) -> pd.DataFrame:
        """Get overall summary statistics"""
        query = f"""
        SELECT 
            COUNT(*) as total_events,
            COUNT(DISTINCT safetyreportid) as unique_reports,
            COUNTIF(serious = '1') as serious_events,
            COUNTIF(serious_death = '1') as deaths,
            COUNTIF(serious_hospitalization = '1') as hospitalizations,
            COUNTIF(serious_death IS NULL AND serious_hospitalization IS NULL AND serious = '0') as mild_events
        FROM `{self.project_id}.{self.dataset_id}.fda_drug_adverse_events`
        """
        return self.query(query)
    
    def get_trends_over_time(self, days: int = 365) -> pd.DataFrame:
        """Get event trends over time"""
        query = f"""
        SELECT 
            PARSE_DATE('%Y%m%d', receivedate) as event_date,
            COUNT(*) as event_count,
            COUNTIF(serious = '1') as serious_count
        FROM `{self.project_id}.{self.dataset_id}.fda_drug_adverse_events`
        WHERE receivedate IS NOT NULL
            AND LENGTH(receivedate) = 8
            AND SAFE.PARSE_DATE('%Y%m%d', receivedate) IS NOT NULL
        GROUP BY event_date
        ORDER BY event_date DESC
        LIMIT {days}
        """
        return self.query(query)
    
    def get_top_drugs(self, limit: int = 20) -> pd.DataFrame:
        """Get drugs with most adverse events"""
        query = f"""
        SELECT 
            REGEXP_EXTRACT(drug_names, r"'([^']+)'") as drug_name,
            COUNT(*) as event_count,
            COUNTIF(serious = '1') as serious_count,
            COUNTIF(serious_death = '1') as death_count,
            ROUND(COUNTIF(serious = '1') * 100.0 / COUNT(*), 1) as serious_percentage
        FROM `{self.project_id}.{self.dataset_id}.fda_drug_adverse_events`
        WHERE drug_names IS NOT NULL AND drug_names != '[]'
        GROUP BY drug_name
        HAVING drug_name IS NOT NULL AND drug_name != ''
        ORDER BY event_count DESC
        LIMIT {limit}
        """
        return self.query(query)
    
    def get_top_reactions(self, limit: int = 20) -> pd.DataFrame:
        """Get most common adverse reactions"""
        query = f"""
        WITH reactions_unnested AS (
            SELECT REGEXP_EXTRACT_ALL(reactions, r"'([^']+)'") as reaction_array
            FROM `{self.project_id}.{self.dataset_id}.fda_drug_adverse_events`
            WHERE reactions IS NOT NULL AND reactions != '[]'
            LIMIT 2000
        )
        SELECT 
            reaction,
            COUNT(*) as count
        FROM reactions_unnested, UNNEST(reaction_array) as reaction
        WHERE reaction != ''
        GROUP BY reaction
        ORDER BY count DESC
        LIMIT {limit}
        """
        return self.query(query)
    
    def get_demographics(self) -> dict:
        """Get patient demographics"""
        # Age distribution
        age_query = f"""
        SELECT 
            CASE 
                WHEN patient_age < 18 THEN 'Under 18'
                WHEN patient_age >= 18 AND patient_age < 30 THEN '18-29'
                WHEN patient_age >= 30 AND patient_age < 45 THEN '30-44'
                WHEN patient_age >= 45 AND patient_age < 65 THEN '45-64'
                WHEN patient_age >= 65 THEN '65+'
                ELSE 'Unknown'
            END as age_group,
            COUNT(*) as count
        FROM `{self.project_id}.{self.dataset_id}.fda_drug_adverse_events`
        WHERE patient_age IS NOT NULL
        GROUP BY age_group
        ORDER BY 
            CASE age_group
                WHEN 'Under 18' THEN 1
                WHEN '18-29' THEN 2
                WHEN '30-44' THEN 3
                WHEN '45-64' THEN 4
                WHEN '65+' THEN 5
                ELSE 6
            END
        """
        
        # Gender distribution
        gender_query = f"""
        SELECT 
            CASE 
                WHEN patient_sex = '1' THEN 'Male'
                WHEN patient_sex = '2' THEN 'Female'
                ELSE 'Unknown'
            END as gender,
            COUNT(*) as count
        FROM `{self.project_id}.{self.dataset_id}.fda_drug_adverse_events`
        GROUP BY gender
        """
        
        return {
            'age': self.query(age_query),
            'gender': self.query(gender_query)
        }
    
    def get_severity_breakdown(self) -> pd.DataFrame:
        """Get breakdown by severity"""
        query = f"""
        SELECT 
            'Deaths' as category,
            COUNT(*) as count
        FROM `{self.project_id}.{self.dataset_id}.fda_drug_adverse_events`
        WHERE serious_death = '1'
        
        UNION ALL
        
        SELECT 
            'Hospitalizations' as category,
            COUNT(*) as count
        FROM `{self.project_id}.{self.dataset_id}.fda_drug_adverse_events`
        WHERE serious_hospitalization = '1'
        
        UNION ALL
        
        SELECT 
            'Life Threatening' as category,
            COUNT(*) as count
        FROM `{self.project_id}.{self.dataset_id}.fda_drug_adverse_events`
        WHERE serious = '1' AND serious_death != '1' AND serious_hospitalization != '1'
        
        UNION ALL
        
        SELECT 
            'Non-Serious' as category,
            COUNT(*) as count
        FROM `{self.project_id}.{self.dataset_id}.fda_drug_adverse_events`
        WHERE serious = '0' OR serious IS NULL
        
        ORDER BY count DESC
        """
        return self.query(query)
    
    def search_events(self, search_term: str, limit: int = 50) -> pd.DataFrame:
        """Search adverse events - improved version"""
        # Clean the search term
        search_term = search_term.strip().lower()
        
        query = f"""
        SELECT 
            safetyreportid,
            receivedate,
            drug_names,
            reactions,
            patient_age,
            patient_sex,
            serious,
            serious_death,
            serious_hospitalization
        FROM `{self.project_id}.{self.dataset_id}.fda_drug_adverse_events`
        WHERE LOWER(CAST(reactions AS STRING)) LIKE '%{search_term}%'
           OR LOWER(CAST(drug_names AS STRING)) LIKE '%{search_term}%'
        LIMIT {limit}
        """
        return self.query(query)
    
    def get_drug_analysis(self, drug_name: str) -> dict:
        """Comprehensive drug analysis"""
        # Basic stats
        stats_query = f"""
        SELECT 
            COUNT(*) as total_events,
            COUNTIF(serious = '1') as serious_events,
            COUNTIF(serious_death = '1') as deaths,
            COUNTIF(serious_hospitalization = '1') as hospitalizations,
            ROUND(AVG(patient_age), 1) as avg_age
        FROM `{self.project_id}.{self.dataset_id}.fda_drug_adverse_events`
        WHERE LOWER(drug_names) LIKE LOWER('%{drug_name}%')
        """
        
        # Top reactions for this drug
        reactions_query = f"""
        WITH reactions_unnested AS (
            SELECT REGEXP_EXTRACT_ALL(reactions, r"'([^']+)'") as reaction_array
            FROM `{self.project_id}.{self.dataset_id}.fda_drug_adverse_events`
            WHERE LOWER(drug_names) LIKE LOWER('%{drug_name}%')
                AND reactions IS NOT NULL AND reactions != '[]'
            LIMIT 500
        )
        SELECT 
            reaction,
            COUNT(*) as count
        FROM reactions_unnested, UNNEST(reaction_array) as reaction
        WHERE reaction != ''
        GROUP BY reaction
        ORDER BY count DESC
        LIMIT 10
        """
        
        # Demographics
        demo_query = f"""
        SELECT 
            patient_sex,
            COUNT(*) as count
        FROM `{self.project_id}.{self.dataset_id}.fda_drug_adverse_events`
        WHERE LOWER(drug_names) LIKE LOWER('%{drug_name}%')
            AND patient_sex IS NOT NULL
        GROUP BY patient_sex
        """
        
        # Events over time
        trend_query = f"""
        SELECT 
            PARSE_DATE('%Y%m%d', receivedate) as event_date,
            COUNT(*) as count
        FROM `{self.project_id}.{self.dataset_id}.fda_drug_adverse_events`
        WHERE LOWER(drug_names) LIKE LOWER('%{drug_name}%')
            AND receivedate IS NOT NULL
            AND LENGTH(receivedate) = 8
            AND SAFE.PARSE_DATE('%Y%m%d', receivedate) IS NOT NULL
        GROUP BY event_date
        ORDER BY event_date DESC
        LIMIT 90
        """
        
        return {
            'stats': self.query(stats_query),
            'reactions': self.query(reactions_query),
            'demographics': self.query(demo_query),
            'trends': self.query(trend_query)
        }
    
    # ==================== Translation ====================
    
    def translate_text(self, text: str, target_lang: str) -> str:
        """Translate text"""
        if not self.translate_client:
            return "Translation API not available"
        
        try:
            result = self.translate_client.translate(text, target_language=target_lang)
            return result['translatedText']
        except Exception as e:
            return f"Translation error: {str(e)}"
    
    # ==================== Speech APIs ====================
    
    def transcribe_audio(self, audio_file) -> str:
        """Transcribe audio"""
        if not self.speech_client:
            return "Speech-to-Text API not available"
        
        try:
            content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                language_code="en-US",
            )
            response = self.speech_client.recognize(config=config, audio=audio)
            
            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript + " "
            
            return transcript.strip() if transcript else "No speech detected"
        except Exception as e:
            return f"Transcription error: {str(e)}"
    
    def synthesize_speech(self, text: str) -> bytes:
        """Text to speech"""
        if not self.tts_client:
            return None
        
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            response = self.tts_client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            return response.audio_content
        except Exception as e:
            st.error(f"TTS error: {str(e)}")
            return None


def main():
    """Main application"""
    
    # Header
    st.markdown('<p class="main-header">🧬 FDA Intelligence Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Comprehensive Drug Safety Analytics | Powered by Google Cloud</p>', unsafe_allow_html=True)
    
    # Initialize
    if 'dashboard' not in st.session_state:
        st.session_state.dashboard = FDADashboard()
    
    dashboard = st.session_state.dashboard
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        project_id = st.text_input("GCP Project ID", value="fda-dashboard-1761298726")
        dataset_id = st.text_input("BigQuery Dataset", value="fda_data")
        
        if st.button("🔗 Connect to Google Cloud", type="primary"):
            with st.spinner("Connecting..."):
                success = dashboard.setup_services(project_id, dataset_id)
                if success:
                    st.session_state.connected = True
        
        st.markdown("---")
        
        if st.session_state.get('connected'):
            st.success("✅ Connected")
            
            # Quick stats
            summary = dashboard.get_overall_summary()
            if not summary.empty:
                st.markdown("### 📊 Quick Stats")
                st.metric("Total Events", f"{summary['total_events'].iloc[0]:,}")
                st.metric("Serious Events", f"{summary['serious_events'].iloc[0]:,}")
                st.metric("Deaths", f"{summary['deaths'].iloc[0]:,}")
    
    # Main content
    if not st.session_state.get('connected'):
        st.info("👈 Connect to Google Cloud using the sidebar to get started")
        return
    
    # Tabs
    tabs = st.tabs([
        "📊 Overview",
        "🔍 Data Explorer",
        "🔎 Search",
        "💊 Drug Analysis",
        "🌐 Translation",
        "🎤 Voice"
    ])
    
    # ==================== TAB 1: Overview Dashboard ====================
    with tabs[0]:
        st.header("📊 Overview Dashboard")
        
        summary = dashboard.get_overall_summary()
        
        if not summary.empty:
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Total Events</div>
                    <div class="metric-value">{summary['total_events'].iloc[0]:,}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Serious Events</div>
                    <div class="metric-value">{summary['serious_events'].iloc[0]:,}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Deaths</div>
                    <div class="metric-value">{summary['deaths'].iloc[0]:,}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Hospitalizations</div>
                    <div class="metric-value">{summary['hospitalizations'].iloc[0]:,}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col5:
                serious_rate = round(summary['serious_events'].iloc[0] / summary['total_events'].iloc[0] * 100, 1)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Serious Rate</div>
                    <div class="metric-value">{serious_rate}%</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏆 Top 20 Drugs")
            top_drugs = dashboard.get_top_drugs(20)
            
            if not top_drugs.empty:
                fig = px.bar(
                    top_drugs,
                    y='drug_name',
                    x='event_count',
                    orientation='h',
                    color='serious_percentage',
                    color_continuous_scale='Reds'
                )
                fig.update_layout(height=600, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("⚠️ Top 20 Reactions")
            reactions = dashboard.get_top_reactions(20)
            
            if not reactions.empty:
                fig = px.treemap(
                    reactions,
                    path=['reaction'],
                    values='count',
                    color='count',
                    color_continuous_scale='Blues'
                )
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
    
    # ==================== TAB 2: Data Explorer ====================
    with tabs[1]:
        st.header("🔍 Data Explorer")
        st.info("Explore what data is available in the database")
        
        # Table stats
        st.subheader("📊 Table Statistics")
        stats = dashboard.get_table_stats()
        
        if not stats.empty:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Rows", f"{stats['total_rows'].iloc[0]:,}")
            col2.metric("Unique Reports", f"{stats['unique_reports'].iloc[0]:,}")
            col3.metric("With Drugs", f"{stats['rows_with_drugs'].iloc[0]:,}")
            col4.metric("With Reactions", f"{stats['rows_with_reactions'].iloc[0]:,}")
        
        st.markdown("---")
        
        # Available drugs
        st.subheader("💊 Top 50 Available Drugs")
        st.info("These are the drugs with most adverse events in the database. Use these names for search.")
        
        drugs = dashboard.get_available_drugs(50)
        if not drugs.empty:
            # Show as searchable table
            st.dataframe(drugs, use_container_width=True, height=400)
            
            # Show as copyable list
            with st.expander("📋 Copy Drug Names"):
                drug_list = ", ".join(drugs['drug_name'].tolist())
                st.code(drug_list, language=None)
        
        st.markdown("---")
        
        # Available reactions
        st.subheader("⚠️ Top 50 Available Reactions")
        st.info("These are the most common reactions in the database. Use these for search.")
        
        reactions = dashboard.get_available_reactions(50)
        if not reactions.empty:
            # Show as searchable table
            st.dataframe(reactions, use_container_width=True, height=400)
            
            # Show as copyable list
            with st.expander("📋 Copy Reaction Names"):
                reaction_list = ", ".join(reactions['reaction'].tolist())
                st.code(reaction_list, language=None)
        
        st.markdown("---")
        
        # Sample data
        st.subheader("📄 Sample Data (First 10 Rows)")
        sample = dashboard.get_data_sample()
        if not sample.empty:
            st.dataframe(sample, use_container_width=True)
    
    # ==================== TAB 3: Search ====================
    with tabs[2]:
        st.header("🔎 Advanced Search")
        st.info("💡 **Tip**: Visit the 'Data Explorer' tab first to see available drugs and reactions!")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_term = st.text_input(
                "Search Term",
                placeholder="Try: aspirin, headache, nausea, pain"
            )
        
        with col2:
            limit = st.selectbox("Results", [10, 25, 50, 100], index=2)
        
        # Show quick suggestions
        st.markdown("**Quick suggestions from your data:**")
        col1, col2, col3 = st.columns(3)
        
        top_drugs = dashboard.get_available_drugs(5)
        top_reactions = dashboard.get_available_reactions(5)
        
        with col1:
            if not top_drugs.empty:
                st.markdown("**Top Drugs:**")
                for drug in top_drugs['drug_name'].head(3):
                    if st.button(f"🔍 {drug}", key=f"drug_{drug}"):
                        search_term = drug
        
        with col2:
            if not top_reactions.empty:
                st.markdown("**Top Reactions:**")
                for reaction in top_reactions['reaction'].head(3):
                    if st.button(f"🔍 {reaction}", key=f"reaction_{reaction}"):
                        search_term = reaction
        
        if st.button("🔎 Search", type="primary") and search_term:
            with st.spinner("Searching..."):
                results = dashboard.search_events(search_term, limit)
                
                if not results.empty:
                    st.success(f"✅ Found {len(results)} results for '{search_term}'")
                    
                    # Summary
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Total", len(results))
                    col2.metric("Serious", results['serious'].eq('1').sum())
                    col3.metric("Deaths", results['serious_death'].eq('1').sum())
                    col4.metric("Hospitalizations", results['serious_hospitalization'].eq('1').sum())
                    
                    st.markdown("---")
                    st.dataframe(results, use_container_width=True, height=600)
                    
                    # Download
                    csv = results.to_csv(index=False)
                    st.download_button(
                        "📥 Download CSV",
                        csv,
                        f"fda_search_{search_term}.csv",
                        "text/csv"
                    )
                else:
                    st.warning(f"⚠️ No results found for '{search_term}'. Try:")
                    st.markdown("- Check the Data Explorer tab for available terms")
                    st.markdown("- Try simpler search terms (single words work best)")
                    st.markdown("- Check spelling")
    
    # ==================== TAB 4: Drug Analysis ====================
    with tabs[3]:
        st.header("💊 Drug Safety Analysis")
        st.info("💡 **Tip**: Get drug names from the 'Data Explorer' tab!")
        
        # Show some suggestions
        top_drugs = dashboard.get_available_drugs(10)
        if not top_drugs.empty:
            st.markdown("**Try analyzing one of these drugs:**")
            cols = st.columns(5)
            for idx, (_, row) in enumerate(top_drugs.head(5).iterrows()):
                with cols[idx]:
                    if st.button(f"💊 {row['drug_name']}", key=f"analyze_{row['drug_name']}"):
                        st.session_state.drug_to_analyze = row['drug_name']
        
        drug_name = st.text_input(
            "Drug Name",
            value=st.session_state.get('drug_to_analyze', ''),
            placeholder="e.g., aspirin, ibuprofen"
        )
        
        if st.button("📊 Analyze", type="primary") and drug_name:
            with st.spinner(f"Analyzing {drug_name}..."):
                analysis = dashboard.get_drug_analysis(drug_name)
                
                if not analysis['stats'].empty and analysis['stats']['total_events'].iloc[0] > 0:
                    stats = analysis['stats'].iloc[0]
                    
                    st.markdown(f"## 💊 {drug_name.title()}")
                    
                    # Metrics
                    col1, col2, col3, col4, col5 = st.columns(5)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Total Events</div>
                            <div class="metric-value">{int(stats['total_events']):,}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Serious</div>
                            <div class="metric-value">{int(stats['serious_events']):,}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Deaths</div>
                            <div class="metric-value">{int(stats['deaths']):,}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col4:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Hospitalizations</div>
                            <div class="metric-value">{int(stats['hospitalizations']):,}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col5:
                        serious_rate = round(stats['serious_events'] / stats['total_events'] * 100, 1)
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Serious Rate</div>
                            <div class="metric-value">{serious_rate}%</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    # Charts
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if not analysis['reactions'].empty:
                            st.subheader("Top Reactions")
                            fig = px.bar(
                                analysis['reactions'],
                                x='count',
                                y='reaction',
                                orientation='h',
                                color='count'
                            )
                            fig.update_layout(height=400, showlegend=False)
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        if not analysis['trends'].empty:
                            st.subheader("Trend (90 Days)")
                            fig = px.line(
                                analysis['trends'],
                                x='event_date',
                                y='count',
                                markers=True
                            )
                            fig.update_layout(height=400)
                            st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning(f"❌ No data found for '{drug_name}'")
                    st.info("💡 Check the Data Explorer tab for available drug names")
    
    # ==================== TAB 5: Translation ====================
    with tabs[4]:
        st.header("🌐 Translation")
        
        if dashboard.translate_client:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                text = st.text_area("Text to Translate", height=200)
            
            with col2:
                lang = st.selectbox(
                    "Language",
                    [
                        ('es', '🇪🇸 Spanish'),
                        ('fr', '🇫🇷 French'),
                        ('de', '🇩🇪 German'),
                        ('zh-CN', '🇨🇳 Chinese'),
                        ('ja', '🇯🇵 Japanese'),
                        ('hi', '🇮🇳 Hindi'),
                        ('ar', '🇸🇦 Arabic')
                    ],
                    format_func=lambda x: x[1]
                )
            
            if st.button("🌍 Translate", type="primary") and text:
                translated = dashboard.translate_text(text, lang[0])
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.markdown(f"### {lang[1]}")
                st.write(translated)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Translation API not available")
    
    # ==================== TAB 6: Voice ====================
    with tabs[5]:
        st.header("🎤 Voice Interface")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎙️ Speech-to-Text")
            if dashboard.speech_client:
                audio_file = st.file_uploader("Upload WAV", type=['wav'])
                if audio_file and st.button("📝 Transcribe"):
                    transcript = dashboard.transcribe_audio(audio_file)
                    st.success("✅ Done!")
                    st.write(transcript)
            else:
                st.warning("Speech-to-Text not available")
        
        with col2:
            st.subheader("🔊 Text-to-Speech")
            if dashboard.tts_client:
                tts_text = st.text_area("Text", height=200)
                if st.button("🎵 Generate") and tts_text:
                    audio = dashboard.synthesize_speech(tts_text)
                    if audio:
                        st.success("✅ Done!")
                        audio_b64 = base64.b64encode(audio).decode()
                        st.markdown(f'<audio controls><source src="data:audio/mp3;base64,{audio_b64}"></audio>', 
                                  unsafe_allow_html=True)
                        st.download_button("📥 Download", audio, "speech.mp3", "audio/mp3")
            else:
                st.warning("Text-to-Speech not available")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p><strong>FDA Intelligence Dashboard v2</strong></p>
        <p>Data source: openFDA | Powered by Google Cloud</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
EOF

# Run the improved version
streamlit run app_final_v2.py --server.port 8501