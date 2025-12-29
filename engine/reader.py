import pdfplumber

def get_text_from_pdf(pdf_file):
    # This function opens the PDF and extracts every word
    with pdfplumber.open(pdf_file) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text()
    return full_text