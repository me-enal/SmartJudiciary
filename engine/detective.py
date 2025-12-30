import re

def find_legal_details(text):
    """
    Specifically tuned for Indian High Court Matrimonial Judgments.
    """
    details = {"Parties": [], "Laws": []}
    
    # We focus on the first 3000 characters where headers usually sit
    header_area = text[:3000]

    # 1. PETITIONER/RESPONDENT PATTERN (The most common High Court format)
    # Looks for: Name ... Appellant/Petitioner VERSUS Name ... Respondent
    formal_pattern = r"(?s)(?:BETWEEN|IN THE MATTER OF:)?\s*(.*?)\s*\.\.\..*?(?:Appellant|Petitioner|Applicant).*?(?:VERSUS|VS\.?|V/S).*?(.*?)\s*\.\.\..*?Respondent"
    formal_match = re.search(formal_pattern, header_area, re.IGNORECASE)

    if formal_match:
        # Clean up the names (remove extra dots, newlines, and professional titles)
        p1 = re.sub(r'[\d\.\n\r]+', ' ', formal_match.group(1)).strip()
        p2 = re.sub(r'[\d\.\n\r]+', ' ', formal_match.group(2)).strip()
        details["Parties"] = [p1[:100], p2[:100]] # Limit length to avoid noise

    # 2. FALLBACK: SIMPLE VS PATTERN (Handles ALL CAPS names)
    if not details["Parties"]:
        vs_pattern = r"([A-Z][A-Z\s]{3,})\s+(?:VERSUS|V/S|VS\.?)\s+([A-Z][A-Z\s]{3,})"
        vs_match = re.search(vs_pattern, header_area)
        if vs_match:
            details["Parties"] = [vs_match.group(1).strip(), vs_match.group(2).strip()]

    # 3. LAW DETECTION
    law_keywords = [
        "Section 125", "CrPC", "Maintenance", "Custody", 
        "Hindu Marriage Act", "Domestic Violence Act", "Section 24"
    ]
    for law in law_keywords:
        if re.search(r'\b' + re.escape(law) + r'\b', text, re.IGNORECASE):
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    """
    Captures formal Indian date formats like '14th October, 2023' or '14.10.2023'.
    """
    # Pattern 1: Numerical dates (DD.MM.YYYY)
    # Pattern 2: Textual dates (14th October 2023)
    date_regex = r'(\d{1,2}(?:st|nd|rd|th)?[\s\.\-/]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]*\d{2,4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    
    matches = re.findall(date_regex, text, re.IGNORECASE)
    
    # Cleaning and sorting unique dates
    unique_dates = list(dict.fromkeys([m.strip() for m in matches]))
    return [f"Scheduled/Occurred: {d}" for d in unique_dates[:10]]





