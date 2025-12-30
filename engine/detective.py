import re

def find_legal_details(text):
    details = {"Parties": [], "Laws": []}
    
    # 1. SEGMENT THE HEADER
    # Most parties are in the first 3000 characters
    header = text[:3000]

    # 2. FORCE-CLEAN THE TEXT
    # This removes all dots, dashes, and extra line breaks that hide the names
    clean_text = re.sub(r'[\.\-\_]+', ' ', header) # Remove dots and dashes
    clean_text = ' '.join(clean_text.split())     # Standardize all spaces

    # 3. ROBUST PARTY SEARCH
    # Looking for Name VS Name or Petitioner vs Respondent
    # Pattern 1: Formal [Name] VERSUS [Name]
    vs_pattern = r"([A-Z][A-Z\s]{3,})\s+(?:VERSUS|V/S|VS\.?)\s+([A-Z][A-Z\s]{3,})"
    
    # Pattern 2: [Name] ... Petitioner ... [Name] ... Respondent
    formal_pattern = r"(.*?)\s*Petitioner\s*.*?\s*(.*?)\s*Respondent"

    match_vs = re.search(vs_pattern, clean_text, re.IGNORECASE)
    match_formal = re.search(formal_pattern, clean_text, re.IGNORECASE)

    if match_vs:
        details["Parties"] = [match_vs.group(1).strip(), match_vs.group(2).strip()]
    elif match_formal:
        details["Parties"] = [match_formal.group(1).strip(), match_formal.group(2).strip()]
    else:
        details["Parties"] = ["Not detected", "Not detected"]

    # 4. LAW DETECTION (This part is working, so we keep it simple)
    law_keywords = ["Section 125", "CrPC", "Maintenance", "Custody", "Hindu Marriage Act"]
    for law in law_keywords:
        if re.search(r'\b' + re.escape(law) + r'\b', text, re.IGNORECASE):
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    # This regex catches: 14.10.2023, 14-10-23, and October 14, 2023
    date_regex = r'(\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}[\s,]+\d{4})'
    
    matches = re.findall(date_regex, text, re.IGNORECASE)
    
    # Get unique dates and clean them
    unique_dates = []
    for m in matches:
        clean_d = m.strip().replace('\n', '')
        if clean_d not in unique_dates:
            unique_dates.append(clean_d)
            
    if not unique_dates:
        return ["No specific dates found"]
    
    return [f"Key Date: {d}" for d in unique_dates[:8]]









