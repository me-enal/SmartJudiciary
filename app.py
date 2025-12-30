import os
import sys
import streamlit as st
import datetime
import spacy
import gc
from sentence_transformers import util

# 1. Path Fix
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 2. Page Configuration (Must be first)
st.set_page_config(page_title="Judiciary AI", page_icon="⚖️", layout="wide")

# 3. Internal Imports
try:
    from engine.reader import get_text_from_pdf
    from engine.detective import find_legal_details, extract_timeline
    from engine.summarizer import make_summary
except ImportError as e:
    st.error(f"Critical Error: {e}")
    st.stop()

# 4. Database Initialization
PAST_CASES = {
    "Suresh v. State of Haryana (2018)": "A landmark case regarding child custody where the welfare of the minor was paramount. The court held that the mother's financial status is not a bar to custody.",
    "Ramesh v. Sunita (2020)": "A case involving Section 125 of CrPC where maintenance was granted to the wife despite her being highly educated but unemployed.",
    "Anjali v. Alok (2021)": "Judgment regarding the division of ancestral property in family disputes under the Hindu Succession Act."
}

# 5. AI Models (Cached)
@st.cache_resource
def load_nlp_model():
    return spacy.load("en_core_web_sm")

@st.cache_resource
def load_bert_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer('all-MiniLM-L6-v2')

research_ai = load_bert_model()
nlp = load_nlp_model()

# 6. Sidebar (EXACTLY AS REQUESTED)
with st.sidebar:
    st.title("⚖️ SmartJudiciary")
    st.subheader("Professional Case Analyzer")
    uploaded_file = st.file_uploader("Upload Judgment PDF", type="pdf")
    st.divider()
    st.info("🔒 Privacy-First: All processing is local.")

# 7. Main UI
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
    
    # 8. Precedent Search (BERT)
    st.subheader("🔍 Finding Precedents (BERT Similarity)")
    current_embedding = research_ai.encode(text[:2000], convert_to_tensor=True)

    with st.expander("View Similar Past Cases", expanded=True):
        found_any = False
        # Initialize session state for learning
        if 'training_data' not in st.session_state:
            st.session_state['training_data'] = PAST_CASES.copy()

        for title, past_text in st.session_state['training_data'].items():
            past_embedding = research_ai.encode(past_text[:2000], convert_to_tensor=True)
            score = util.cos_sim(current_embedding, past_embedding).item()
            
            if score > 0.40:
                st.write(f"✅ **{title}** - Similarity: {int(score*100)}%")
                st.caption(f"Legal Context: {past_text[:150]}...")
                found_any = True
        
        if not found_any:
            st.info("No highly similar precedents found in the current database.")

    # 9. Results Display (2 Columns - EXACTLY AS REQUESTED)
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
        
        # Export Feature
        st.divider()
        st.subheader("📥 Export Case Brief")
        report_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timeline_string = "\n".join(timeline_events)
        full_report = f"⚖️ JUDICIARY AI CASE BRIEF\nGenerated: {report_timestamp}\n\nSUMMARY:\n{summary}\n\nTIMELINE:\n{timeline_string}"
        
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

# 10. Enhanced Learning (Feedback Loop)
st.divider()
st.subheader("🤖 Improve AI Decision Making")

if 'training_data' not in st.session_state:
    st.session_state['training_data'] = PAST_CASES.copy()

with st.expander("Contribute this case to AI Training?"):
    st.write("By contributing, you help the model recognize similar legal patterns in the future.")
    case_name = st.text_input("Enter a name for this case:")
    
    if st.button("Authorize & Train Model"):
        if case_name and uploaded_file:
            st.session_state['training_data'][case_name] = text[:5000]
            st.success(f"Successfully added '{case_name}' to the training set!")
            st.balloons()
        else:
            st.warning("Please upload a file and provide a name.")

gc.collect()collect()


















