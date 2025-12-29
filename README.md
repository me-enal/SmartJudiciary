\# ⚖️ SmartJudiciary: AI Family Law Assistant



An AI-powered system designed to analyze Indian Family Law judgments. This tool automates the process of reading long legal PDFs, extracting key parties, and generating case summaries.



\## 🚀 Features

\- \*\*PDF Extraction:\*\* Reads complex legal documents using `pdfplumber`.

\- \*\*Legal Entity Detection:\*\* Identifies Petitioners, Respondents, and Acts (e.g., Hindu Marriage Act).

\- \*\*Automated Chronology:\*\* Extracts dates to build a case timeline.

\- \*\*AI Summarization:\*\* Uses Transformer models (BART) for actionable case briefs.



\## 🛠️ Setup Instructions

1\. Clone the repo: `git clone https://github.com/YOUR\_USERNAME/SmartJudiciary.git`

2\. Install dependencies: `pip install -r requirements.txt`

3\. Download the AI model: `python -m spacy download en\_core\_web\_trf`

4\. Run the app: `streamlit run app.py`



\## 📦 Tech Stack

\- \*\*Frontend:\*\* Streamlit

\- \*\*NLP:\*\* spaCy \& Hugging Face Transformers

\- \*\*PDF Engine:\*\* pdfplumber

