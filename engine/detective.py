import re

def find_legal_details(text):
    details = {"Parties": [], "Laws": []}
    
    # 1. SCAN THE HEADER (First 4000 characters)
    header = text[:4000]
    
    # CLEANING: Remove long sequences of dots and standardize whitespace
    clean_header = re.sub(r'\.{2,}', ' ', header)
    clean_header = ' '.join(clean_header.split())

    # 2. PARTY DETECTION - STRATEGY A: VS/VERSUS
    vs_pattern = r"([A-Z][A-Z\s]{3,})\s+(?:VERSUS|V/S|VS\.?)\s+([A-Z][A-Z\s]{3,})"
    match_vs = re.search(vs_pattern, clean_header, re.IGNORECASE)

    # 3. PARTY DETECTION - STRATEGY B: PETITIONER/RESPONDENT ANCHORS
    # This looks for names located before the word 'Petitioner' or 'Appellant'
    pet_pattern = r"([A-Z][A-Z\s]{3,})(?=\s*[\(\[].*?(?:Petitioner|Appellant|Plaintiff))"
    res_pattern = r"([A-Z][A-Z\s]{3,})(?=\s*[\(\[].*?(?:Respondent|Defendant))"
    
    match_pet = re.search(pet_pattern, clean_header, re.IGNORECASE)
    match_res = re.search(res_pattern, clean_header, re.IGNORECASE)

    if match_vs:
        details["Parties"] = [match_vs.group(1).strip(), match_vs.group(2).strip()]
    elif match_pet and match_res:
        details["Parties"] = [match_pet.group(1).strip(), match_res.group(1).strip()]
    else:
        # Final fallback: Look for anything in ALL CAPS that looks like a name
        caps_names = re.findall(r'\b[A-Z]{4,}(?:\s[A-Z]{4,})*\b', clean_header)
        if len(caps_names) >= 2:
            details["Parties"] = [caps_names[0], caps_names[1]]
        else:
            details["Parties"] = ["Not detected", "Not detected"]

    # 4. LAW DETECTION (This is working, so we keep it stable)
    law_keywords = ["Section 125", "CrPC", "Maintenance", "Custody", "Hindu Marriage Act"]
    for law in law_keywords:
        if re.search(r'\b' + re.escape(law) + r'\b', text, re.IGNORECASE):
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    # This regex is now much wider to catch '14th October 2023' or '14.10.2023'
    date_regex = r'(\d{1,2}(?:st|nd|rd|th)?[\s\.\-/]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]*\d{2,4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    
    matches = re.findall(date_regex, text, re.IGNORECASE)
    
    # Clean and filter unique dates
    unique_dates = []
    for m in matches:
        clean_d = m.strip()
        if clean_d not in unique_dates:
            unique_dates.append(clean_d)
            
    if not unique_dates:
        return ["No specific dates found"]
    
    return [f"Key Date: {d}" for d in unique_dates[:8]]










