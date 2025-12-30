import os
import sys
import streamlit as st
import datetime
import spacy
import gc
from sentence_transformers import util

# 1. Path Fix
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 2. Page Configuration (Simplified to one line to avoid SyntaxErrors)
st.set_page_config(page_title="Judiciary AI", page_icon="⚖️", layout="wide")

# 3. Internal Imports
try:
    from engine.reader import get_text_from_pdf
    from engine.detective import find_legal_details, extract_timeline
    from engine.summarizer import make_summary
except ImportError as e:
    st.error(f"Folder Error: {e}")
    st.stop()

# 4. Database Initialization
if 'training_data' not in st.session_state:
    st.session_state['training_data'] = {
        "Suresh v. State of Haryana (2018)": "Child custody case focused on minor welfare.",
        "Ramesh v. Sunita (2020)": "Maintenance granted to wife under Section 125 CrPC.",
        "Anjali v. Alok (2021)": "Ancestral property division under Hindu Succession Act."
    }

# 5. AI Models (Cached)
@st.cache_resource
def load_nlp():
    return spacy.load("en_core_web_sm")

@st.cache_resource
def load_bert():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer('all-MiniLM-L6-v2')

nlp = load_nlp()
research_ai = load_bert()

# 6. Sidebar
with st.sidebar:
    st.title("⚖️ SmartJudiciary")
    uploaded_file = st.file_uploader("Upload Judgment PDF", type="pdf")
    st.info("🔒 Privacy-First Processing")

# 7. Main UI
st.title("Judiciary AI System for Family Law")

if uploaded_file:
    with st.status("🚀 Processing...", expanded=True) as status:
        text = get_text_from_pdf(uploaded_file)
        details = find_legal_details(text)
        timeline_events = extract_timeline(text)
        summary = make_summary(text)
        status.update(label="Complete!", state="complete")

    # 8. Precedent Search
    st.subheader("🔍 Finding Precedents")
    current_emb = research_ai.encode(text[:2000], convert_to_tensor=True)
    
    with st.expander("Similar Past Cases", expanded=True):
        for title, past_text in st.session_state['training_data'].items():
            past_emb = research_ai.encode(past_text[:2000], convert_to_tensor=True)
            score = util.cos_sim(current_emb, past_emb).item()
            if score > 0.35:
                st.write(f"✅ **{title}** ({int(score*100)}% match)")

    # 9. Results
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📌 Key Entities")
        st.write(f"**Parties:** {', '.join(details['Parties'])}")
        st.write(f"**Laws:** {', '.join(details['Laws'])}")
    with col2:
        st.subheader("📝 Summary")
        st.info(summary)

    # 10. Learning Section
    st.divider()
    with st.expander("🤖 Train AI with this case?"):
        c_name = st.text_input("Case Name:")
        if st.button("Train Now"):
            st.session_state['training_data'][c_name] = text[:5000]
            st.success("AI learned new patterns!")
            st.balloons()
else:
    st.info("Upload a PDF to begin.")

gc.collect()

















