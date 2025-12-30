import sys
import os
import streamlit as st
import datetime
import spacy
import pdfplumber
import gc
from sentence_transformers import util

# Custom Engine Imports
from engine.reader import get_text_from_pdf
from engine.detective import find_legal_details, extract_timeline
from engine.summarizer import make_summary
from engine.database import PAST_CASES 

# 1. Page Configuration (This MUST be the first Streamlit command)
st.set_page_config(
    page_title="Judiciary AI: Family Law Assistant",
    page_icon="⚖️",
    layout="wide"
)

# --- AI MODEL LOADING ---
@st.cache_resource
def load_nlp_model():
    return spacy.load("en_core_web_sm")

@st.cache_resource
def load_bert_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer('all-MiniLM-L6-v2')

research_ai = load_bert_model()
nlp = load_nlp_model()

# --- Sidebar ---
with st.sidebar:
    st.title("⚖️ SmartJudiciary")
    st.subheader("Professional Case Analyzer")
    uploaded_file = st.file_uploader("Upload Judgment PDF", type="pdf")
    st.divider()
    st.info("🔒 Privacy-First: All processing is local.")

# --- Main Header ---
st.title("Judiciary AI System for Family Law")
st.markdown("---")

if uploaded_file:
    # --- PROCESSING ---
    with st.status("🚀 AI Engine Processing...", expanded=True) as status:
        st.write("📖 Reading PDF content...")
        text = get_text_from_pdf(uploaded_file)
        
        st.write("🕵️ Detecting Parties and Legal Provisions...")
        details = find_legal_details(text)
        
        st.write("⏳ Reconstructing Case Timeline...")
        timeline_events = extract_timeline(text)
        
        st.write("📝 Synthesizing Actionable Summary...")
        summary = make_summary(text)
        
        status.update(label="Analysis Complete!", state="complete", expanded=False)

    # --- SIMILARITY SEARCH (Now correctly indented inside the 'if' block) ---
    st.subheader("🔍 Finding Precedents (BERT Similarity)")
    current_embedding = research_ai.encode(text[:2000], convert_to_tensor=True)

    with st.expander("View Similar Past Cases", expanded=True):
        for title, past_text in PAST_CASES.items():
            past_embedding = research_ai.encode(past_text[:2000], convert_to_tensor=True)
            score = util.cos_sim(current_embedding, past_embedding).item()
            
            if score > 0.40:
                st.write(f"✅ **{title}** - Similarity: {int(score*100)}%")
                st.caption(f"Legal Context: {past_text[:120]}...")

    # --- RESULTS SECTION ---
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📌 Key Case Entities")
        st.success(f"**Parties:** {', '.join(details['Parties']) if details['Parties'] else 'Not detected'}")
        st.warning(f"**Laws & Acts:** {', '.join(details['Laws']) if details['Laws'] else 'Not detected'}")
        
        st.subheader("⏳ Case Chronology")
        if timeline_events:
            for event in timeline_events:
                st.markdown(event)
        else:
            st.info("No specific dates found in text.")

    with col2:
        st.subheader("📝 Actionable Summary")
        st.info(summary)
        
        st.divider()
        st.subheader("📥 Export Case Brief")
        report_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_report = f"""
⚖️ JUDICIARY AI CASE BRIEF
Generated on: {report_timestamp}
---------------------------------------
FILE NAME: {uploaded_file.name}
PARTIES: {', '.join(details['Parties'])}
SUMMARY: {summary}
---------------------------------------
"""
        st.download_button(
            label="Download Case Brief (.txt)",
            data=full_report,
            file_name=f"Case_Brief_{uploaded_file.name.replace('.pdf', '')}.txt",
            mime="text/plain"
        )

else:
    # --- LANDING PAGE ---
    st.image("https://via.placeholder.com/1000x300.png?text=Upload+a+Legal+PDF+to+Start+Analysis", use_column_width=True)
    st.write("### How to use:")
    st.write("1. Upload a PDF judgment in the left sidebar.")
    st.write("2. Wait for the AI to extract parties, dates, and laws.")

# Final memory cleanup at the bottom
gc.collect()








