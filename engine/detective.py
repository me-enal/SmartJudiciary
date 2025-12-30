import re

def find_legal_details(text):
    details = {"Parties": [], "Laws": []}
    
    # Focus on the first 3000 characters
    header = text[:3000]
    
    # 1. CLEANING: Remove the dots and legal titles that confuse the AI
    # This turns "MEENAL ... Appellant" into "MEENAL Appellant"
    clean_header = re.sub(r'\.{2,}', ' ', header)
    clean_header = ' '.join(clean_header.split())

    # 2. THE "DEEP SCAN" FOR NAMES
    # This looks for a Name VERSUS Name pattern first
    vs_pattern = r"([A-Z][A-Z\s]{3,})\s+(?:VERSUS|V/S|VS\.?)\s+([A-Z][A-Z\s]{3,})"
    match_vs = re.search(vs_pattern, clean_header, re.IGNORECASE)

    if match_vs:
        p1, p2 = match_vs.group(1).strip(), match_vs.group(2).strip()
    else:
        # If no VS, look for names trapped before Petitioner/Respondent markers
        # We capture everything BEFORE the word Petitioner that is in ALL CAPS
        pet_pattern = r"\b([A-Z\s]{4,})\b(?=\s*[\(\[].*?(?:Petitioner|Appellant|Plaintiff))"
        res_pattern = r"\b([A-Z\s]{4,})\b(?=\s*[\(\[].*?(?:Respondent|Defendant))"
        
        m_pet = re.search(pet_pattern, clean_header)
        m_res = re.search(res_pattern, clean_header)
        
        p1 = m_pet.group(1).strip() if m_pet else "Not detected"
        p2 = m_res.group(1).strip() if m_res else "Not detected"

    # 3. FINAL CLEANUP: Remove "THE", "APPELLANT", etc. if they got caught
    noise = ["THE ", "APPELLANT", "PETITIONER", "RESPONDENT", "VERSUS", "VS", "V/S"]
    for word in noise:
        p1 = re.sub(rf'\b{word}\b', '', p1, flags=re.IGNORECASE).strip()
        p2 = re.sub(rf'\b{word}\b', '', p2, flags=re.IGNORECASE).strip()

    details["Parties"] = [p1, p2]

    # 4. LAW DETECTION
    law_keywords = ["Section 125", "CrPC", "Maintenance", "Custody", "Hindu Marriage Act"]
    for law in law_keywords:
        if re.search(r'\b' + re.escape(law) + r'\b', text, re.IGNORECASE):
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    # This regex handles dates like '14th October 2023' or '14.10.2023'
    date_regex = r'(\d{1,2}(?:st|nd|rd|th)?[\s\.\-/]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]*\d{2,4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    matches = re.findall(date_regex, text, re.IGNORECASE)
    unique_dates = list(dict.fromkeys([m.strip() for m in matches]))
    return [f"Key Date: {d}" for d in unique_dates[:8]]











