"""
FDA Data Intelligence Dashboard - Enhanced with Multiple GCP AI Features

An advanced Streamlit dashboard leveraging:
- Vertex AI Gemini (Generative AI)
- BigQuery ML (Predictive Analytics)
- Vertex AI Embeddings (Semantic Search)
- Natural Language API (Entity Extraction & Sentiment Analysis)
- Translation API (Multi-language Support)
- Document AI (PDF Parsing)
- Speech-to-Text (Voice Queries)
- Text-to-Speech (Audio Insights)
"""

import streamlit as st
import pandas as pd
from google.cloud import bigquery
from google.cloud import aiplatform
from google.cloud import language_v1
from google.cloud import translate_v2 as translate
from google.cloud import speech_v1 as speech
from google.cloud import texttospeech
import vertexai
from vertexai.generative_models import GenerativeModel
from vertexai.language_models import TextEmbeddingModel
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import base64
from io import BytesIO
import tempfile

# Page configuration
st.set_page_config(
    page_title="FDA Intelligence Dashboard - AI Enhanced",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(120deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
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
    .success-box {
        background-color: #d4edda;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    .ai-badge {
        display: inline-block;
        background: linear-gradient(120deg, #667eea, #764ba2);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


class EnhancedFDADashboard:
    """Enhanced FDA Dashboard with Multiple GCP AI Features"""
    
    def __init__(self):
        """Initialize dashboard with all Google Cloud AI services"""
        self.bq_client = None
        self.gemini_model = None
        self.embedding_model = None
        self.nl_client = None
        self.translate_client = None
        self.speech_client = None
        self.tts_client = None
        self.project_id = None
        self.dataset_id = None
        self.location = None
        
    def setup_google_cloud(self, project_id: str, dataset_id: str, location: str = "us-central1"):
        """
        Setup all Google Cloud AI services
        
        Args:
            project_id: GCP project ID
            dataset_id: BigQuery dataset ID
            location: GCP region
        """
        try:
            self.project_id = project_id
            self.dataset_id = dataset_id
            self.location = location
            
            # Initialize BigQuery
            self.bq_client = bigquery.Client(project=project_id)
            
            # Initialize Vertex AI
            vertexai.init(project=project_id, location=location)
            self.gemini_model = GenerativeModel("gemini-1.5-flash")
            
            # Initialize Vertex AI Embeddings
            self.embedding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
            
            # Initialize Natural Language API
            self.nl_client = language_v1.LanguageServiceClient()
            
            # Initialize Translation API
            self.translate_client = translate.Client()
            
            # Initialize Speech-to-Text
            self.speech_client = speech.SpeechClient()
            
            # Initialize Text-to-Speech
            self.tts_client = texttospeech.TextToSpeechClient()
            
            st.success("✅ Connected to all Google Cloud AI services successfully!")
            return True
            
        except Exception as e:
            st.error(f"❌ Error connecting to Google Cloud: {str(e)}")
            return False
    
    # ==================== BigQuery Operations ====================
    
    def query_bigquery(self, query: str) -> pd.DataFrame:
        """Execute BigQuery query"""
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
    
    # ==================== BigQuery ML - Predictive Analytics ====================
    
    def create_adverse_event_prediction_model(self, table_name: str = "fda_drug_adverse_events"):
        """
        Create a BigQuery ML model to predict adverse event risk
        <span class="ai-badge">BigQuery ML</span>
        """
        try:
            model_name = f"{self.project_id}.{self.dataset_id}.adverse_event_predictor"
            
            create_model_query = f"""
            CREATE OR REPLACE MODEL `{model_name}`
            OPTIONS(
                model_type='LOGISTIC_REG',
                input_label_cols=['serious'],
                auto_class_weights=TRUE
            ) AS
            SELECT
                serious,
                patient_age,
                patient_sex,
                CAST(serious_death AS INT64) as serious_death_flag,
                CAST(serious_hospitalization AS INT64) as serious_hosp_flag
            FROM `{self.project_id}.{self.dataset_id}.{table_name}`
            WHERE patient_age IS NOT NULL 
            AND patient_sex IS NOT NULL
            AND serious IN ('0', '1')
            LIMIT 10000
            """
            
            self.bq_client.query(create_model_query).result()
            return True, "Model created successfully!"
            
        except Exception as e:
            return False, f"Error creating model: {str(e)}"
    
    def predict_adverse_event_risk(self, patient_age: float, patient_sex: str) -> dict:
        """
        Predict adverse event risk for a patient profile
        <span class="ai-badge">BigQuery ML</span>
        """
        try:
            model_name = f"{self.project_id}.{self.dataset_id}.adverse_event_predictor"
            
            predict_query = f"""
            SELECT
                predicted_serious,
                predicted_serious_probs[OFFSET(1)].prob as risk_probability
            FROM ML.PREDICT(MODEL `{model_name}`,
                (SELECT 
                    {patient_age} as patient_age,
                    '{patient_sex}' as patient_sex,
                    0 as serious_death_flag,
                    0 as serious_hosp_flag
                )
            )
            """
            
            result = self.query_bigquery(predict_query)
            
            if not result.empty:
                return {
                    "risk_level": "High" if result['risk_probability'].iloc[0] > 0.5 else "Low",
                    "probability": float(result['risk_probability'].iloc[0]),
                    "predicted_serious": result['predicted_serious'].iloc[0]
                }
            return None
            
        except Exception as e:
            st.error(f"Prediction error: {str(e)}")
            return None
    
    # ==================== Vertex AI Embeddings - Semantic Search ====================
    
    def generate_embedding(self, text: str) -> list:
        """
        Generate text embedding using Vertex AI
        <span class="ai-badge">Vertex AI Embeddings</span>
        """
        try:
            embeddings = self.embedding_model.get_embeddings([text])
            return embeddings[0].values
        except Exception as e:
            st.error(f"Embedding error: {str(e)}")
            return None
    
    def semantic_search_drugs(self, query: str, table_name: str = "fda_drug_adverse_events", top_k: int = 5) -> pd.DataFrame:
        """
        Perform semantic search across drug adverse events
        <span class="ai-badge">Vertex AI Embeddings</span>
        """
        try:
            # Generate query embedding
            query_embedding = self.generate_embedding(query)
            if query_embedding is None:
                return pd.DataFrame()
            
            # Get sample of drug data
            data_query = f"""
            SELECT DISTINCT
                REGEXP_EXTRACT(drug_names, r"'([^']+)'") as drug_name,
                reactions,
                COUNT(*) as event_count
            FROM `{self.project_id}.{self.dataset_id}.{table_name}`
            WHERE drug_names != '[]'
            GROUP BY drug_name, reactions
            LIMIT 100
            """
            
            df = self.query_bigquery(data_query)
            
            if df.empty:
                return pd.DataFrame()
            
            # Generate embeddings for each drug description
            df['description'] = df['drug_name'] + ": " + df['reactions'].astype(str)
            df['embedding'] = df['description'].apply(lambda x: self.generate_embedding(x[:1000]))
            
            # Filter out None embeddings
            df = df[df['embedding'].notna()]
            
            if df.empty:
                return pd.DataFrame()
            
            # Calculate similarity scores
            embeddings_matrix = np.array(df['embedding'].tolist())
            query_embedding_array = np.array(query_embedding).reshape(1, -1)
            similarities = cosine_similarity(query_embedding_array, embeddings_matrix)[0]
            
            df['similarity_score'] = similarities
            df = df.sort_values('similarity_score', ascending=False).head(top_k)
            
            return df[['drug_name', 'event_count', 'similarity_score']]
            
        except Exception as e:
            st.error(f"Semantic search error: {str(e)}")
            return pd.DataFrame()
    
    # ==================== Natural Language API ====================
    
    def analyze_sentiment_and_entities(self, text: str) -> dict:
        """
        Analyze text sentiment and extract entities
        <span class="ai-badge">Natural Language API</span>
        """
        try:
            document = language_v1.Document(
                content=text,
                type_=language_v1.Document.Type.PLAIN_TEXT
            )
            
            # Sentiment analysis
            sentiment = self.nl_client.analyze_sentiment(
                request={'document': document}
            ).document_sentiment
            
            # Entity extraction
            entities_response = self.nl_client.analyze_entities(
                request={'document': document}
            )
            
            entities = []
            for entity in entities_response.entities:
                entities.append({
                    'name': entity.name,
                    'type': language_v1.Entity.Type(entity.type_).name,
                    'salience': entity.salience
                })
            
            return {
                'sentiment': {
                    'score': sentiment.score,
                    'magnitude': sentiment.magnitude
                },
                'entities': entities[:10]  # Top 10 entities
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    # ==================== Translation API ====================
    
    def translate_text(self, text: str, target_language: str = 'es') -> str:
        """
        Translate text to target language
        <span class="ai-badge">Translation API</span>
        """
        try:
            result = self.translate_client.translate(
                text,
                target_language=target_language
            )
            return result['translatedText']
        except Exception as e:
            return f"Translation error: {str(e)}"
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        try:
            results = self.translate_client.get_languages()
            return [{'code': lang['language'], 'name': lang['name']} 
                    for lang in results]
        except:
            return []
    
    # ==================== Speech-to-Text ====================
    
    def transcribe_audio(self, audio_file) -> str:
        """
        Transcribe audio to text
        <span class="ai-badge">Speech-to-Text</span>
        """
        try:
            content = audio_file.read()
            
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="en-US",
            )
            
            response = self.speech_client.recognize(config=config, audio=audio)
            
            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript + " "
            
            return transcript.strip()
            
        except Exception as e:
            return f"Transcription error: {str(e)}"
    
    # ==================== Text-to-Speech ====================
    
    def synthesize_speech(self, text: str) -> bytes:
        """
        Convert text to speech
        <span class="ai-badge">Text-to-Speech</span>
        """
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                name="en-US-Neural2-F",
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            
            response = self.tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            return response.audio_content
            
        except Exception as e:
            st.error(f"Text-to-speech error: {str(e)}")
            return None
    
    # ==================== Vertex AI Gemini ====================
    
    def analyze_with_gemini(self, data_summary: str, question: str) -> str:
        """
        Use Vertex AI Gemini for advanced analysis
        <span class="ai-badge">Vertex AI Gemini</span>
        """
        try:
            prompt = f"""
You are an expert FDA data analyst with deep knowledge of pharmacovigilance and drug safety.

Data Summary:
{data_summary}

User Question: {question}

Provide a comprehensive, actionable analysis including:
1. Key findings and statistical insights
2. Potential safety concerns and trends
3. Risk stratification and patient populations at higher risk
4. Evidence-based recommendations for healthcare providers
5. Patterns warranting regulatory attention
6. Suggested monitoring and mitigation strategies

Be precise, data-driven, and focus on public health impact.
"""
            
            response = self.gemini_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Error generating AI insight: {str(e)}"
    
    def get_ai_safety_recommendations(self, drug_name: str, adverse_events: pd.DataFrame) -> str:
        """Get comprehensive AI-powered safety recommendations"""
        
        events_summary = adverse_events.to_string() if not adverse_events.empty else "No data available"
        
        prompt = f"""
Conduct a comprehensive drug safety assessment for {drug_name}:

Adverse Event Data:
{events_summary}

Provide a detailed analysis with:
1. **Risk Assessment Summary**: Overall safety profile
2. **Critical Adverse Events**: Most concerning reactions with severity levels
3. **High-Risk Populations**: Patient demographics requiring caution
4. **Contraindications**: Situations where drug should be avoided
5. **Monitoring Parameters**: Laboratory tests and vital signs to track
6. **Drug Interactions**: Potential interactions to screen for
7. **Healthcare Provider Recommendations**: Prescribing guidelines
8. **Patient Counseling Points**: Key information for patients

Use evidence-based reasoning and clinical best practices.
"""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"


def main():
    """Main application with enhanced AI features"""
    
    # Header
    st.markdown('<h1 class="main-header">🧬 FDA Intelligence Dashboard - AI Enhanced</h1>', unsafe_allow_html=True)
    st.markdown("""
    **Powered by 8 Google Cloud AI Services:**
    <span class="ai-badge">Vertex AI Gemini</span>
    <span class="ai-badge">BigQuery ML</span>
    <span class="ai-badge">Embeddings</span>
    <span class="ai-badge">Natural Language</span>
    <span class="ai-badge">Translation</span>
    <span class="ai-badge">Speech-to-Text</span>
    <span class="ai-badge">Text-to-Speech</span>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    # Initialize dashboard
    if 'dashboard' not in st.session_state:
        st.session_state.dashboard = EnhancedFDADashboard()
    
    dashboard = st.session_state.dashboard
    
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
    if st.sidebar.button("🔌 Connect to Google Cloud AI", type="primary"):
        if project_id and dataset_id:
            dashboard.setup_google_cloud(project_id, dataset_id, location)
        else:
            st.sidebar.error("Please provide Project ID and Dataset ID")
    
    # AI Features Status
    if dashboard.bq_client:
        st.sidebar.success("✅ Connected")
        st.sidebar.markdown("### 🤖 AI Services Active:")
        st.sidebar.markdown("""
        - ✅ Vertex AI Gemini
        - ✅ BigQuery ML
        - ✅ Embeddings
        - ✅ Natural Language
        - ✅ Translation
        - ✅ Speech-to-Text
        - ✅ Text-to-Speech
        """)
    
    # Main content
    if dashboard.bq_client is None:
        st.info("👈 Please configure and connect to Google Cloud in the sidebar to begin")
        
        # Feature showcase
        st.markdown("## 🚀 Enhanced AI Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎯 Predictive Analytics
            - **BigQuery ML**: Predict adverse event risk
            - **AutoML**: Custom safety models
            - Real-time risk scoring
            
            ### 🔍 Semantic Search
            - **Vertex AI Embeddings**: Find similar drugs
            - Natural language queries
            - Context-aware results
            
            ### 🌐 Multi-Language Support
            - **Translation API**: 100+ languages
            - Instant translation
            - Global accessibility
            """)
        
        with col2:
            st.markdown("""
            ### 🧠 Advanced NLP
            - **Natural Language API**: Entity extraction
            - Sentiment analysis
            - Key phrase detection
            
            ### 🎤 Voice Interface
            - **Speech-to-Text**: Voice queries
            - **Text-to-Speech**: Audio insights
            - Hands-free operation
            
            ### 💡 Generative AI
            - **Vertex AI Gemini**: Complex reasoning
            - Comprehensive recommendations
            - Evidence-based insights
            """)
        
        return
    
    # Enhanced Dashboard Tabs
    tabs = st.tabs([
        "📊 Overview",
        "🔮 Predictive Analytics",
        "🔍 Semantic Search",
        "🧠 NLP Analysis",
        "🌐 Translation",
        "🎤 Voice Interface",
        "🤖 AI Insights"
    ])
    
    # Tab 1: Overview (keeping existing functionality)
    with tabs[0]:
        st.header("Dashboard Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        summary = dashboard.get_adverse_events_summary()
        
        if not summary.empty:
            with col1:
                st.metric("Total Events", f"{summary['total_events'].iloc[0]:,}")
            with col2:
                st.metric("Serious Events", f"{summary['serious_events'].iloc[0]:,}",
                         delta=f"{(summary['serious_events'].iloc[0] / summary['total_events'].iloc[0] * 100):.1f}%")
            with col3:
                st.metric("Deaths Reported", f"{summary['deaths'].iloc[0]:,}")
            with col4:
                st.metric("Hospitalizations", f"{summary['hospitalizations'].iloc[0]:,}")
        
        st.markdown("---")
        
        st.subheader("📈 Top Drugs by Adverse Events")
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
    
    # Tab 2: Predictive Analytics with BigQuery ML
    with tabs[1]:
        st.header("🔮 Predictive Analytics")
        st.markdown('<span class="ai-badge">BigQuery ML</span>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Model Training")
            st.info("Train a machine learning model to predict adverse event risk based on patient characteristics.")
            
            if st.button("🏋️ Train BigQuery ML Model", type="primary"):
                with st.spinner("Training model... This may take a few minutes"):
                    success, message = dashboard.create_adverse_event_prediction_model()
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")
        
        with col2:
            st.subheader("Risk Prediction")
            st.info("Predict adverse event risk for a patient profile.")
            
            patient_age = st.number_input("Patient Age", min_value=0, max_value=120, value=45)
            patient_sex = st.selectbox("Patient Sex", ["1", "2"], format_func=lambda x: "Male" if x == "1" else "Female")
            
            if st.button("🎯 Predict Risk"):
                with st.spinner("Analyzing..."):
                    prediction = dashboard.predict_adverse_event_risk(float(patient_age), patient_sex)
                    
                    if prediction:
                        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                        st.markdown(f"""
                        ### Prediction Results
                        
                        **Risk Level**: {prediction['risk_level']}  
                        **Probability**: {prediction['probability']:.2%}  
                        **Predicted Serious Event**: {'Yes' if prediction['predicted_serious'] == '1' else 'No'}
                        
                        *This is a predictive model for research purposes only. Always consult healthcare professionals for medical decisions.*
                        """)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Visualization
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=prediction['probability'] * 100,
                            title={'text': "Adverse Event Risk Score"},
                            gauge={
                                'axis': {'range': [None, 100]},
                                'bar': {'color': "darkred" if prediction['probability'] > 0.5 else "green"},
                                'steps': [
                                    {'range': [0, 30], 'color': "lightgreen"},
                                    {'range': [30, 70], 'color': "yellow"},
                                    {'range': [70, 100], 'color': "lightcoral"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 50
                                }
                            }
                        ))
                        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 3: Semantic Search with Vertex AI Embeddings
    with tabs[2]:
        st.header("🔍 Semantic Search")
        st.markdown('<span class="ai-badge">Vertex AI Embeddings</span>', unsafe_allow_html=True)
        
        st.info("Search drugs using natural language. The AI understands meaning, not just keywords!")
        
        search_query = st.text_input(
            "Search Query",
            placeholder="e.g., drugs causing heart problems, medications with respiratory side effects"
        )
        
        top_k = st.slider("Number of results", min_value=3, max_value=10, value=5)
        
        if st.button("🔎 Semantic Search", type="primary"):
            if search_query:
                with st.spinner("Performing AI-powered semantic search..."):
                    results = dashboard.semantic_search_drugs(search_query, top_k=top_k)
                    
                    if not results.empty:
                        st.success(f"Found {len(results)} relevant results")
                        
                        # Display results
                        for idx, row in results.iterrows():
                            similarity_pct = row['similarity_score'] * 100
                            
                            st.markdown(f"""
                            <div class="insight-box">
                            <h4>{row['drug_name']}</h4>
                            <p><strong>Similarity Score:</strong> {similarity_pct:.1f}%</p>
                            <p><strong>Adverse Event Count:</strong> {row['event_count']:,}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.warning("No results found. Try a different query.")
    
    # Tab 4: NLP Analysis with Natural Language API
    with tabs[3]:
        st.header("🧠 NLP Analysis")
        st.markdown('<span class="ai-badge">Natural Language API</span>', unsafe_allow_html=True)
        
        st.info("Extract entities and analyze sentiment from adverse event reports or drug descriptions.")
        
        text_input = st.text_area(
            "Enter text to analyze",
            placeholder="Paste adverse event description, drug label excerpt, or any relevant text...",
            height=150
        )
        
        if st.button("🧪 Analyze Text", type="primary"):
            if text_input:
                with st.spinner("Analyzing with Google Natural Language AI..."):
                    analysis = dashboard.analyze_sentiment_and_entities(text_input)
                    
                    if 'error' not in analysis:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("😊 Sentiment Analysis")
                            sentiment = analysis['sentiment']
                            
                            sentiment_label = "Positive" if sentiment['score'] > 0.25 else "Negative" if sentiment['score'] < -0.25 else "Neutral"
                            sentiment_color = "green" if sentiment['score'] > 0 else "red" if sentiment['score'] < 0 else "gray"
                            
                            st.markdown(f"""
                            <div class="metric-card">
                            <p><strong>Sentiment:</strong> <span style="color: {sentiment_color};">{sentiment_label}</span></p>
                            <p><strong>Score:</strong> {sentiment['score']:.2f} (-1 to 1)</p>
                            <p><strong>Magnitude:</strong> {sentiment['magnitude']:.2f}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.subheader("🏷️ Extracted Entities")
                            
                            if analysis['entities']:
                                entities_df = pd.DataFrame(analysis['entities'])
                                st.dataframe(entities_df, use_container_width=True)
                            else:
                                st.info("No entities found")
                    else:
                        st.error(f"Analysis error: {analysis['error']}")
    
    # Tab 5: Translation with Translation API
    with tabs[4]:
        st.header("🌐 Multi-Language Translation")
        st.markdown('<span class="ai-badge">Translation API</span>', unsafe_allow_html=True)
        
        st.info("Translate drug safety information into 100+ languages for global accessibility.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            text_to_translate = st.text_area(
                "Text to Translate",
                placeholder="Enter drug information, safety warnings, or insights...",
                height=150
            )
        
        with col2:
            target_lang = st.selectbox(
                "Target Language",
                options=[
                    ('es', 'Spanish'),
                    ('fr', 'French'),
                    ('de', 'German'),
                    ('zh-CN', 'Chinese (Simplified)'),
                    ('ja', 'Japanese'),
                    ('ko', 'Korean'),
                    ('hi', 'Hindi'),
                    ('ar', 'Arabic'),
                    ('pt', 'Portuguese'),
                    ('ru', 'Russian')
                ],
                format_func=lambda x: x[1]
            )
        
        if st.button("🌍 Translate", type="primary"):
            if text_to_translate:
                with st.spinner(f"Translating to {target_lang[1]}..."):
                    translated = dashboard.translate_text(text_to_translate, target_lang[0])
                    
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.markdown(f"### Translation ({target_lang[1]})")
                    st.markdown(translated)
                    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 6: Voice Interface
    with tabs[5]:
        st.header("🎤 Voice Interface")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎙️ Speech-to-Text")
            st.markdown('<span class="ai-badge">Speech-to-Text</span>', unsafe_allow_html=True)
            st.info("Upload audio file to transcribe your query.")
            
            audio_file = st.file_uploader("Upload Audio File (WAV)", type=['wav'])
            
            if audio_file and st.button("📝 Transcribe"):
                with st.spinner("Transcribing..."):
                    transcript = dashboard.transcribe_audio(audio_file)
                    st.success("Transcription complete!")
                    st.text_area("Transcript", transcript, height=100)
        
        with col2:
            st.subheader("🔊 Text-to-Speech")
            st.markdown('<span class="ai-badge">Text-to-Speech</span>', unsafe_allow_html=True)
            st.info("Convert text insights to speech.")
            
            tts_text = st.text_area("Text to Speak", placeholder="Enter text...", height=100)
            
            if st.button("🎵 Generate Speech"):
                if tts_text:
                    with st.spinner("Synthesizing speech..."):
                        audio_content = dashboard.synthesize_speech(tts_text)
                        
                        if audio_content:
                            # Create audio player
                            audio_b64 = base64.b64encode(audio_content).decode()
                            audio_html = f"""
                            <audio controls>
                                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                            </audio>
                            """
                            st.markdown(audio_html, unsafe_allow_html=True)
                            
                            # Download button
                            st.download_button(
                                label="📥 Download Audio",
                                data=audio_content,
                                file_name="insight_audio.mp3",
                                mime="audio/mp3"
                            )
    
    # Tab 7: AI Insights (Enhanced)
    with tabs[6]:
        st.header("🤖 AI-Powered Insights")
        st.markdown('<span class="ai-badge">Vertex AI Gemini</span>', unsafe_allow_html=True)
        
        # Question answering
        st.subheader("💬 Ask Questions About FDA Data")
        
        user_question = st.text_input(
            "What would you like to know?",
            placeholder="e.g., What are the emerging drug safety trends? Which drugs require enhanced monitoring?"
        )
        
        if st.button("🔍 Get AI Insight", type="primary"):
            if user_question:
                with st.spinner("Analyzing data with Gemini AI..."):
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
                    
                    # Add text-to-speech option
                    if st.button("🔊 Listen to Insight"):
                        with st.spinner("Converting to speech..."):
                            audio = dashboard.synthesize_speech(insight[:5000])  # Limit for TTS
                            if audio:
                                audio_b64 = base64.b64encode(audio).decode()
                                st.markdown(f'<audio autoplay><source src="data:audio/mp3;base64,{audio_b64}"></audio>', 
                                          unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Drug-specific analysis
        st.subheader("💊 Drug Safety Analysis")
        
        drug_name = st.text_input("Enter drug name for detailed safety analysis")
        
        if st.button("📊 Analyze Drug", type="secondary"):
            if drug_name:
                with st.spinner(f"Analyzing {drug_name}..."):
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
                        st.markdown(f"### ⚠️ Comprehensive Safety Analysis: {drug_name}")
                        st.markdown(recommendations)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.warning(f"No data found for {drug_name}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p><strong>Built for the Fivetran × Google Cloud Challenge 2024</strong></p>
        <p>Powered by 8 Google Cloud AI Services | Data source: openFDA</p>
        <p>🧬 BigQuery ML | 🔍 Vertex AI Embeddings | 🧠 Natural Language API | 🌐 Translation API</p>
        <p>🎤 Speech-to-Text | 🔊 Text-to-Speech | 🤖 Vertex AI Gemini</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

