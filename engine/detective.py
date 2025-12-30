import re

def find_legal_details(text):
    # Safety check: if text is empty, the PDF is a scan/image
    if not text or len(text.strip()) < 20:
        return {"Parties": ["PDF MIGHT BE A SCAN", "CANNOT READ IMAGE"], "Laws": ["No text detected"]}

    details = {"Parties": ["Not detected", "Not detected"], "Laws": []}
    
    # 1. Split into lines and remove empty ones
    lines = [l.strip() for l in text[:3000].split('\n') if len(l.strip()) > 2]

    # 2. THE HUNTER: Look for keywords like Petitioner/Respondent
    p1_found = False
    p2_found = False

    for i, line in enumerate(lines):
        # Look for Petitioner/Appellant
        if not p1_found and any(word in line.upper() for word in ["PETITIONER", "APPELLANT", "PLAINTIFF"]):
            # Grab this line, but clean off the "..."
            details["Parties"][0] = line.split('...')[0].strip()
            p1_found = True
        
        # Look for Respondent/Defendant
        if not p2_found and any(word in line.upper() for word in ["RESPONDENT", "DEFENDANT"]):
            details["Parties"][1] = line.split('...')[0].strip()
            p2_found = True

    # 3. THE SAFETY NET: If keywords failed, just take the top lines
    # Usually, Line 4 is the Petitioner and Line 10 is the Respondent
    if not p1_found and len(lines) > 4:
        details["Parties"][0] = lines[3]
    if not p2_found and len(lines) > 8:
        details["Parties"][1] = lines[8]

    # 4. LAW DETECTION
    for law in ["Section 125", "Maintenance", "Hindu Marriage Act", "Custody", "CrPC", "HMA"]:
        if law.lower() in text.lower():
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    # Pulls any sequence that looks like a date
    date_regex = r'(\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    found = re.findall(date_regex, text)
    # Also look for years
    years = re.findall(r'\b(19|20)\d{2}\b', text[:2000])
    
    combined = list(dict.fromkeys(found + years))
    return [f"Date/Year found: {d}" for d in combined[:6]] if combined else ["No dates detected"]




















