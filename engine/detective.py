import re

def find_legal_details(text):
    details = {"Parties": ["Not detected", "Not detected"], "Laws": []}
    
    # 1. Get the very top of the document
    header = text[:2000]
    
    # 2. Look for the 'VERSUS' line
    # We split the text into lines to find what is above and below VERSUS
    lines = [l.strip() for l in header.split('\n') if len(l.strip()) > 2]
    
    vs_index = -1
    for i, line in enumerate(lines):
        if "VERSUS" in line.upper() or "V/S" in line.upper() or " VS " in line.upper():
            vs_index = i
            break
            
    if vs_index != -1:
        # The Petitioner is usually the first non-empty line above VERSUS
        # The Respondent is usually the first non-empty line below VERSUS
        if vs_index > 0:
            details["Parties"][0] = lines[vs_index - 1].split('...')[0].strip()
        if vs_index < len(lines) - 1:
            details["Parties"][1] = lines[vs_index + 1].split('...')[0].strip()
    else:
        # Fallback: Just look for the first two lines that are in ALL CAPS
        caps_lines = [l for l in lines if l.isupper() and len(l.split()) < 6][:2]
        if len(caps_lines) >= 2:
            details["Parties"] = caps_lines

    # 3. Simple Law Detection
    keywords = ["Section 125", "Maintenance", "Custody", "CrPC", "HMA"]
    for k in keywords:
        if k.lower() in text.lower():
            details["Laws"].append(k)
            
    return details

def extract_timeline(text):
    # This finds any date like 10.12.2023 or 10/12/2023 or 10-12-2023
    # It also finds dates like 10th October 2023
    date_pattern = r'(\d{1,2}(?:st|nd|rd|th)?[\s\.\-/]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]*\d{2,4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    matches = re.findall(date_pattern, text, re.IGNORECASE)
    
    unique_dates = []
    for m in matches:
        if m not in unique_dates:
            unique_dates.append(m)
            
    if not unique_dates:
        return ["No dates found in the first few pages"]
        
    return [f"Date: {d}" for d in unique_dates[:5]]


















