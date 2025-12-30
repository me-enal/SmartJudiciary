import re

def find_legal_details(text):
    details = {"Parties": [], "Laws": []}
    
    # 1. PRE-CLEANING (The Secret Sauce)
    # We take the first 3000 chars and remove all long sequences of dots and extra newlines
    # This turns "MEENAL ..... VS ..... RAJESH" into "MEENAL VS RAJESH"
    clean_head = re.sub(r'\.{2,}', ' ', text[:3000]) # Remove 2+ dots
    clean_head = re.sub(r'\s+', ' ', clean_head)    # Remove extra spaces/newlines

    # 2. THE "FIRST CODE" LOGIC (Strict & Simple)
    # This looks for any words separated by VS, VERSUS, or V/S
    party_pattern = r"([A-Z][A-Z\s]{2,})\s+(?:VERSUS|VS\.?|V/S)\s+([A-Z][A-Z\s]{2,})"
    
    match = re.search(party_pattern, clean_head, re.IGNORECASE)

    if match:
        p1 = match.group(1).strip()
        p2 = match.group(2).strip()
        
        # Remove common court noise from names
        for noise in ["PETITIONER", "APPELLANT", "RESPONDENT", "PLAINTIFF", "AND ORS", "AND OTHERS"]:
            p1 = re.sub(rf'\b{noise}\b', '', p1, flags=re.IGNORECASE).strip()
            p2 = re.sub(rf'\b{noise}\b', '', p2, flags=re.IGNORECASE).strip()
            
        details["Parties"] = [p1, p2]
    else:
        # Emergency Fallback: If no VS is found, try to find "Petitioner"
        pet_match = re.search(r"([A-Z][A-Z\s]{2,})\s+.*?PETITIONER", clean_head, re.IGNORECASE)
        res_match = re.search(r"([A-Z][A-Z\s]{2,})\s+.*?RESPONDENT", clean_head, re.IGNORECASE)
        if pet_match and res_match:
            details["Parties"] = [pet_match.group(1).strip(), res_match.group(1).strip()]
        else:
            details["Parties"] = ["Not detected", "Not detected"]

    # 3. LAW DETECTION (Keep what is working)
    law_keywords = ["Section 125", "CrPC", "Maintenance", "Custody", "Hindu Marriage Act", "Domestic Violence"]
    for law in law_keywords:
        if law.lower() in text.lower():
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    # This pattern catches 14.10.2023, 14/10/2023, and October 14, 2023
    date_regex = r'(\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4}|(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}[\s,]+\d{4})'
    
    matches = re.findall(date_regex, text, re.IGNORECASE)
    
    unique_dates = []
    for m in matches:
        if m not in unique_dates:
            unique_dates.append(m)
            
    if not unique_dates:
        return ["No specific dates found"]
    
    return [f"Key Date: {d}" for d in unique_dates[:8]]








