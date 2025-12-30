import re

def find_legal_details(text):
    details = {"Parties": [], "Laws": []}
    
    # We only look at the start of the document for parties
    header = text[:3000]

    # 1. THE ORIGINAL SUCCESSFUL LOGIC (Simplified)
    # This looks for Name ... VS ... Name
    # The [^.]+ means "match everything except dots" to stop it from grabbing dots
    party_pattern = r"([A-Z][A-Z\s]+)(?:\.|\s)+(?:VERSUS|VS\.?|V/S)(?:\.|\s)+([A-Z][A-Z\s]+)"
    
    match = re.search(party_pattern, header, re.IGNORECASE)

    if match:
        # Clean the names of any leftover dots or "Petitioner" labels
        p1 = match.group(1).replace('.', '').strip()
        p2 = match.group(2).replace('.', '').strip()
        
        # Remove common court labels if they got caught in the name
        for label in ["PETITIONER", "APPELLANT", "RESPONDENT", "PLAINTIFF"]:
            p1 = p1.upper().replace(label, "").strip()
            p2 = p2.upper().replace(label, "").strip()
            
        details["Parties"] = [p1, p2]
    else:
        details["Parties"] = ["Not detected", "Not detected"]

    # 2. LAW DETECTION (This part is working well for you)
    law_keywords = ["Section 125", "CrPC", "Maintenance", "Custody", "Hindu Marriage Act"]
    for law in law_keywords:
        if law.lower() in text.lower():
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    # Expanded date regex to catch "14.10.2023" and "October 14, 2023"
    date_regex = r'(\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}[\s,]+\d{4})'
    matches = re.findall(date_regex, text, re.IGNORECASE)
    
    unique_dates = []
    for m in matches:
        if m not in unique_dates:
            unique_dates.append(m)
            
    if not unique_dates:
        return ["No dates found"]
    
    return [f"Key Date: {d}" for d in unique_dates[:5]]







