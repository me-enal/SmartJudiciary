import re

def find_legal_details(text):
    details = {"Parties": ["Not detected", "Not detected"], "Laws": []}
    
    # 1. Get the first 20 lines of the document
    lines = [l.strip() for l in text[:2000].split('\n') if len(l.strip()) > 3]
    
    # 2. THE 'VERSUS' ANCHOR SEARCH
    vs_idx = -1
    for i, line in enumerate(lines):
        if re.search(r'\b(VERSUS|V/S|VS)\b', line, re.I):
            vs_idx = i
            break
            
    if vs_idx != -1:
        # Petitioner is 1-2 lines above VERSUS
        # Respondent is 1-2 lines below VERSUS
        p1_raw = lines[vs_idx - 1] if vs_idx > 0 else "Not detected"
        p2_raw = lines[vs_idx + 1] if vs_idx < len(lines)-1 else "Not detected"
        
        def clean_name(name):
            # If name is in brackets (Anjali Sharma), take that
            match = re.search(r'\(([^)]+)\)', name)
            if match:
                name = match.group(1)
            # Remove titles and noise
            name = re.sub(r'\b(SMT|SHRI|MR|MS|MRS|APPELLANT|RESPONDENT|PETITIONER|THE|AND|VERSUS|VS)\b', '', name, flags=re.I)
            name = re.sub(r'[^a-zA-Z\s]', '', name)
            return name.strip().upper()

        details["Parties"] = [clean_name(p1_raw), clean_name(p2_raw)]

    # 3. EMERGENCY FALLBACK
    # If VS wasn't found, just grab the first two lines that look like names
    if details["Parties"][0] == "" or details["Parties"][0] == "NOT DETECTED":
        # Filter out lines that are clearly just addresses or dates
        potential_names = [l for l in lines if not any(word in l.upper() for word in ["COURT", "JUDGE", "DATED", "ADVOCATE", "STREET", "ROAD", "INCOME"])][:2]
        if len(potential_names) >= 2:
            details["Parties"] = [potential_names[0].upper(), potential_names[1].upper()]

    # 4. LAW DETECTION
    laws = ["Section 125", "Maintenance", "Hindu Marriage Act", "Custody", "CrPC"]
    for law in laws:
        if re.search(r'\b' + re.escape(law) + r'\b', text, re.I):
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    # Powerful date search
    date_regex = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}[\s,]+\d{4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    found = re.findall(date_regex, text, re.I)
    unique_dates = list(dict.fromkeys([d.strip() for d in found]))
    return [f"Key Date: {d}" for d in unique_dates[:8]] if unique_dates else ["No dates found"]






























