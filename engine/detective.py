import re

def find_legal_details(text):
    details = {"Parties": ["Not detected", "Not detected"], "Laws": []}
    
    # 1. Get the first 3000 characters and split into lines
    lines = [line.strip() for line in text[:3000].split('\n') if len(line.strip()) > 1]
    
    # 2. FIND THE PARTIES
    # We look for the line that has "VERSUS" or "VS"
    vs_idx = -1
    for i, line in enumerate(lines):
        if re.search(r'\b(VERSUS|V/S|VS)\b', line, re.I):
            vs_idx = i
            break
            
    if vs_idx != -1:
        # Petitioner is the line directly above VERSUS
        if vs_idx > 0:
            details["Parties"][0] = lines[vs_idx - 1].replace('...', '').strip()
        # Respondent is the line directly below VERSUS
        if vs_idx < len(lines) - 1:
            details["Parties"][1] = lines[vs_idx + 1].replace('...', '').strip()
    
    # Fallback: If no VS is found, take the first two lines that are in CAPITAL LETTERS
    if details["Parties"][0] == "Not detected":
        caps_lines = [l for l in lines if l.isupper() and len(l.split()) < 6]
        if len(caps_lines) >= 2:
            details["Parties"] = caps_lines[:2]

    # 3. FIND THE LAWS
    law_keywords = ["Section 125", "CrPC", "Maintenance", "Hindu Marriage Act", "HMA", "Custody", "Domestic Violence"]
    for law in law_keywords:
        if law.lower() in text.lower():
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    # This regex is a 'Vacuum' - it sucks up any date it finds
    # Matches: 12.10.2023, 12/10/2023, 12th October 2023, October 12, 2023
    date_regex = r'(\d{1,2}(?:st|nd|rd|th)?[\s\.\-/]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]*\d{2,4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    
    found_dates = re.findall(date_regex, text, re.I)
    
    # Keep only unique dates to keep it clean
    unique_dates = []
    for d in found_dates:
        if d not in unique_dates:
            unique_dates.append(d)
            
    if not unique_dates:
        return ["No dates found in header"]
        
    return [f"Key Date: {d}" for d in unique_dates[:6]]



















