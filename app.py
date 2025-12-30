import sys
import os
import streamlit as st
import datetime
import spacy
import gc
from sentence_transformers import util

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Judiciary AI: Family Law Assistant",
    page_icon="⚖️",
    layout="wide"
)

# --- 2. PAST CASES DATABASE (Embedded so it never fails) ---
# You can add more cases to this dictionary later
PAST_CASES = {
    "Suresh v. State of Haryana (2018)": "A landmark case regarding child custody where the welfare of the minor was paramount. The court held that the mother's financial status is not a bar to custody.",
    "Ramesh v. Sunita (2020)": "A case involving Section 125 of CrPC where maintenance was granted to the wife despite her being highly educated but unemployed.",
    "Anjali v. Alok (2021)": "Judgment regarding the division of ancestral property in family disputes under the Hindu Succession Act."
}

# --- 3. CUSTOM ENGINE IMPORTS ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from engine.reader import get_text_from_pdf
from engine.detective import find_legal_details, extract_timeline
from engine.summarizer import make_summary

# --- 4. AI MODELS (Cached) ---
@st.cache_resource
def load_nlp_model():
    return spacy.load("en_core_web_sm")

@st.cache_resource
def load_bert_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer('all-MiniLM-L6-v2')

research_ai = load_bert_model()
nlp = load_nlp_model()

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("⚖️ SmartJudiciary")
    st.subheader("Professional Case Analyzer")
    uploaded_file = st.file_uploader("Upload Judgment PDF", type="pdf")
    st.divider()
    st.info("🔒 Privacy-First: All processing is local.")

# --- 6. MAIN UI ---
st.title("Judiciary AI System for Family Law")
st.markdown("---")

if uploaded_file:
    # Processing Status
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

    st.markdown("---")
    
    # 7. PRECEDENT SEARCH (BERT)
    st.subheader("🔍 Finding Precedents (BERT Similarity)")
    
    # Analyze the first 2000 characters of the uploaded document
    current_embedding = research_ai.encode(text[:2000], convert_to_tensor=True)

    with st.expander("View Similar Past Cases", expanded=True):
        found_any = False
        for title, past_text in PAST_CASES.items():
            past_embedding = research_ai.encode(past_text[:2000], convert_to_tensor=True)
            score = util.cos_sim(current_embedding, past_embedding).item()
            
            # Show cases with more than 40% similarity
            if score > 0.40:
                st.write(f"✅ **{title}** - Similarity: {int(score*100)}%")
                st.caption(f"Legal Context: {past_text[:150]}...")
                found_any = True
        
        if not found_any:
            st.info("No highly similar precedents found in the current database.")

    # 8. RESULTS DISPLAY (2 Columns)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📌 Key Case Entities")
        st.success(f"**Parties:** {', '.join(details['Parties']) if details['Parties'] else 'Not detected'}")
        st.warning(f"**Laws & Acts:** {', '.join(details['Laws']) if details['Laws'] else 'Not detected'}")
        
        st.subheader("⏳ Case Chronology")
        if timeline_events:
            for event in timeline_events:
                st.markdown(f"• {event}")
        else:
            st.info("No specific dates found in text.")

    with col2:
        st.subheader("📝 Actionable Summary")
        st.info(summary)
        
        # 9. EXPORT FEATURE
        st.divider()
        st.subheader("📥 Export Case Brief")
        
        report_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_report = f"""
⚖️ JUDICIARY AI CASE BRIEF
Generated on: {report_timestamp}
---------------------------------------
FILE NAME: {uploaded_file.name}

PARTIES: {', '.join(details['Parties'])}
LEGAL PROVISIONS: {', '.join(details['Laws'])}

SUMMARY:
{summary}

CHRONOLOGY:
{chr(10).join(timeline_events)}
---------------------------------------
End of Brief.
        """
        
        st.download_button(
            label="Download Case Brief (.txt)",
            data=full_report,
            file_name=f"Case_Brief_{uploaded_file.name.replace('.pdf', '')}.txt",
            mime="text/plain"
        )

else:
    # Landing Page
    st.image("https://via.placeholder.com/1000x300.png?text=Upload+a+Legal+PDF+to+Start+Analysis", use_column_width=True)
    st.write("### How to use:")
    st.write("1. Upload a PDF judgment in the left sidebar.")
    st.write("2. Wait for the AI to extract parties, dates, and laws.")
    st.write("3. Review the summary and precedents below.")

# Memory Cleanup
gc.collect()










