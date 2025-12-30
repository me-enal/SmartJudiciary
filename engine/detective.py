import re

def find_legal_details(text):
    """
    Final optimized detector for Indian High Court Judgment formats.
    """
    details = {"Parties": [], "Laws": []}
    
    # 1. ROBUST PARTY DETECTION (The 'Between/Versus' Logic)
    # We search the first 4000 chars for the formal header
    header = text[:4000]

    # Pattern: Captures names followed by 'Appellant/Petitioner/Applicant' 
    # and names followed by 'Respondent', separated by 'VERSUS'
    # The (?s) flag allows matching across multiple lines
    formal_regex = r"(?s)(?:BETWEEN|MATTER OF|CASE OF)?\s*(.*?)\s*(?:\.\.\.|–)\s*(?:Appellant|Petitioner|Applicant|Plaintiff).*?(?:VERSUS|VS\.?|V/S).*?(.*?)\s*(?:\.\.\.|–)\s*Respondent"
    
    match = re.search(formal_regex, header, re.IGNORECASE)

    if match:
        # Cleanup: Remove dots, 'Mr./Ms.', and extra spaces
        p1 = re.sub(r'[\.\d\n\r\t]+', ' ', match.group(1)).strip()
        p2 = re.sub(r'[\.\d\n\r\t]+', ' ', match.group(2)).strip()
        
        # Final polish to remove common titles
        titles = ["MR ", "MS ", "MRS ", "SHRI ", "SMT ", "MD "]
        for t in titles:
            p1 = p1.upper().replace(t, "")
            p2 = p2.upper().replace(t, "")
            
        details["Parties"] = [p1.strip(), p2.strip()]
    
    # Fallback: Simple 'A VS B' on one line
    if not details["Parties"]:
        simple_vs = r"([A-Z][A-Z\s]+)\s+(?:VERSUS|VS\.?|V/S)\s+([A-Z][A-Z\s]+)"
        simple_match = re.search(simple_vs, header)
        if simple_match:
            details["Parties"] = [simple_match.group(1).strip(), simple_match.group(2).strip()]

    # 2. LAW DETECTION (Existing logic is working, adding minor improvements)
    law_keywords = [
        "Section 125", "CrPC", "Maintenance", "Custody", 
        "Hindu Marriage Act", "Domestic Violence Act", "Section 24",
        "Hindu Succession Act", "Guardians and Wards Act"
    ]
    for law in law_keywords:
        if re.search(r'\b' + re.escape(law) + r'\b', text, re.IGNORECASE):
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    """
    Advanced date parser for Indian Court date formats.
    """
    # Pattern 1: Numerical (14.10.2023)
    # Pattern 2: Alpha (14th October 2023)
    # Pattern 3: Alpha-Reverse (October 14, 2023)
    date_regex = r'(\d{1,2}(?:st|nd|rd|th)?[\s\.\-/]*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]*\d{2,4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}[\s,]+\d{4})'
    
    matches = re.findall(date_regex, text, re.IGNORECASE)
    
    # Clean and remove duplicates
    unique_dates = []
    for m in matches:
        clean_date = m.strip().replace('\n', ' ')
        if clean_date not in unique_dates:
            unique_dates.append(clean_date)
            
    return [f"Key Date: {d}" for d in unique_dates[:8]]






