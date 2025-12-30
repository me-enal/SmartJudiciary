import os
import sys
import streamlit as st
import datetime
import gc
from sentence_transformers import util

# 1. Path Fix
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 2. Internal Imports
try:
    from engine.reader import get_text_from_pdf
    from engine.detective import find_legal_details, extract_timeline
    from engine.summarizer import make_summary
except ImportError:
    PAST_CASES = {} 

# 3. Page Configuration (EXACTLY AS YOU HAD IT)
st.set_page_config(
    page_title="Judiciary AI",
    page_icon="⚖️",
    layout="wide"
)

PAST_CASES = {
    "Suresh v. State of Haryana (2018)": "A landmark case regarding child custody where the welfare of the minor was paramount. The court held that the mother's financial status is not a bar to custody.",
    "Ramesh v. Sunita (2020)": "A case involving Section 125 of CrPC where maintenance was granted to the wife despite her being highly educated but unemployed.",
    "Anjali v. Alok (2021)": "Judgment regarding the division of ancestral property in family disputes under the Hindu Succession Act."
}

# --- 4. AI MODELS (Memory-Optimized Loaders) ---
@st.cache_resource
def load_nlp_model():
    import spacy
    # Permanent Fix: Disable heavy features to save 300MB RAM
    return spacy.load("en_core_web_sm", disable=["parser", "ner"])

@st.cache_resource
def load_bert_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer('all-MiniLM-L6-v2')

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
    # Wake up models only when file is present
    research_ai = load_bert_model()
    
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
    
    # Analyze the first 1500 characters to stay under memory limit
    current_embedding = research_ai.encode(text[:1500], convert_to_tensor=True)

    with st.expander("View Similar Past Cases", expanded=True):
        found_any = False
        if 'training_data' not in st.session_state:
            st.session_state['training_data'] = PAST_CASES.copy()

        for title, past_text in st.session_state['training_data'].items():
            past_embedding = research_ai.encode(past_text[:1500], convert_to_tensor=True)
            score = util.cos_sim(current_embedding, past_embedding).item()
            
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
        # Format timeline for text file
        timeline_str = "\n".join(timeline_events)
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
{timeline_str}
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

# --- 10. ENHANCED LEARNING SECTION ---
st.divider()
st.subheader("🤖 Improve AI Decision Making")

if 'training_data' not in st.session_state:
    st.session_state['training_data'] = PAST_CASES.copy()

with st.expander("Contribute this case to AI Training?"):
    st.write("By contributing, you help the model recognize similar legal patterns in the future.")
    case_name = st.text_input("Enter a name for this case (e.g., Party A vs Party B):")
    
    if st.button("Authorize & Train Model"):
        if case_name:
            st.session_state['training_data'][case_name] = text[:3000]
            st.success(f"Successfully added '{case_name}' to the local training set!")
            st.balloons()
        else:
            st.warning("Please provide a case name first.")

# Final Memory Cleanup
gc.collect()



















