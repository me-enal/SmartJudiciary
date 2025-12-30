import sys
import os
import streamlit as st
import datetime
import spacy
import pdfplumber
import gc
from sentence_transformers import util

# 1. Page Configuration (MUST be the first Streamlit command)
st.set_page_config(
    page_title="Judiciary AI: Family Law Assistant",
    page_icon="⚖️",
    layout="wide"
)

# Custom Engine Imports
from engine.reader import get_text_from_pdf
from engine.detective import find_legal_details, extract_timeline
from engine.summarizer import make_summary
from engine.database import PAST_CASES 

# --- AI MODEL LOADING (Zero spaces at the start of @ lines) ---
@st.cache_resource
def load_nlp_model():
    return spacy.load("en_core_web_sm")

@st.cache_resource
def load_bert_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer('all-MiniLM-L6-v2')

# Initialize the brains
research_ai = load_bert_model()
nlp = load_nlp_model()

# --- UI START ---
st.title("Smart Judiciary AI")

with st.sidebar:
    st.title("⚖️ SmartJudiciary")
    st.subheader("Professional Case Analyzer")
    uploaded_file = st.file_uploader("Upload Judgment PDF", type="pdf")
    st.divider()
    st.info("🔒 Privacy-First Processing")

st.markdown("---")

if uploaded_file:
    with st.status("🚀 AI Engine Processing...", expanded=True) as status:
        st.write("📖 Reading PDF content...")
        text = get_text_from_pdf(uploaded_file)
        
        st.write("🕵️ Detecting Parties...")
        details = find_legal_details(text)
        
        st.write("⏳ Reconstructing Timeline...")
        timeline_events = extract_timeline(text)
        
        st.write("📝 Synthesizing Summary...")
        summary = make_summary(text)
        
        status.update(label="Analysis Complete!", state="complete", expanded=False)

    # --- SIMILARITY SEARCH ---
    st.subheader("🔍 Finding Precedents (BERT Similarity)")
    current_embedding = research_ai.encode(text[:2000], convert_to_tensor=True)

    with st.expander("View Similar Past Cases", expanded=True):
        for title, past_text in PAST_CASES.items():
            past_embedding = research_ai.encode(past_text[:2000], convert_to_tensor=True)
            score = util.cos_sim(current_embedding, past_embedding).item()
            
            if score > 0.40:
                st.write(f"✅ **{title}** - Similarity: {int(score*100)}%")
                st.caption(f"Legal Context: {past_text[:120]}...")

    # --- RESULTS DISPLAY ---
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📌 Key Case Entities")
        st.success(f"**Parties:** {', '.join(details['Parties']) if details['Parties'] else 'Not detected'}")
        st.warning(f"**Laws & Acts:** {', '.join(details['Laws']) if details['Laws'] else 'Not detected'}")
        
        st.subheader("⏳ Case Chronology")
        if timeline_events:
            for event in timeline_events:
                st.markdown(event)

    with col2:
        st.subheader("📝 Actionable Summary")
        st.info(summary)
        
        st.divider()
        st.subheader("📥 Export Case Brief")
        st.download_button(
            label="Download Case Brief (.txt)",
            data=f"SUMMARY:\n{summary}",
            file_name="Case_Brief.txt",
            mime="text/plain"
        )

else:
    st.info("Please upload a PDF file in the sidebar to begin.")

# Final memory cleanup
gc.collect()









