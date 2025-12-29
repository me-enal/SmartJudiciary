import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
from engine.reader import get_text_from_pdf
from engine.detective import find_legal_details, extract_timeline
from engine.summarizer import make_summary
import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="Judiciary AI: Family Law Assistant",
    page_icon="⚖️",
    layout="wide"
)

# 2. Sidebar - Branding and Upload
with st.sidebar:
    st.title("⚖️ SmartJudiciary")
    st.subheader("Professional Case Analyzer")
    uploaded_file = st.file_uploader("Upload Judgment PDF", type="pdf")
    st.divider()
    st.info("🔒 Privacy-First: All processing is local. No data leaves your machine.")

# 3. Main Header
st.title("Judiciary AI System for Family Law")
st.markdown("---")

if uploaded_file:
    # Status bar for the user to track AI steps
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

    # 4. Results Section: Displaying in 2 Columns
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
        
        # 5. Export Feature for Lawyers
        st.divider()
        st.subheader("📥 Export Case Brief")
        
        # Prepare the text for the download file
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
            mime="text/plain",
            help="Download the summary and timeline for court use."
        )

else:
    # Landing Page view
    st.image("https://via.placeholder.com/1000x300.png?text=Upload+a+Legal+PDF+to+Start+Analysis", use_column_width=True)
    st.write("### How to use:")
    st.write("1. Upload a PDF judgment in the left sidebar.")
    st.write("2. Wait for the AI to extract parties, dates, and laws.")

    st.write("3. Review the summary and download the final Case Brief for your records.")
