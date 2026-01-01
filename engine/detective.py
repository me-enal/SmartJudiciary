import re

def find_legal_details(text):
    # 1. Check if text actually exists
    if not text or len(text.strip()) < 10:
        return {"Parties": ["PDF UNREADABLE", "CHECK IF SCAN"], "Laws": []}

    # 2. Extract first 15 lines (more cushion for headers)
    lines = [l.strip() for l in text[:3000].split('\n') if len(l.strip()) > 2]
    
    found = []
    
    # 3. Look for names in brackets
    for line in lines:
        match = re.search(r'\(([^)]+)\)', line)
        if match:
            name = match.group(1).strip().upper()
            # Filter out legal roles
            if not any(x in name for x in ["APPELLANT", "RESPONDENT", "PETITIONER", "PLAINTIFF", "DEFENDANT"]):
                if name not in found: # Fix duplication
                    found.append(name)

    # 4. Fallback: If we don't have 2 names, scan for lines that DON'T have noise
    if len(found) < 2:
        noise = ["COURT", "JUDGE", "VERSUS", "VS", "V/S", "ORDER", "JUDGMENT", "DATED"]
        for line in lines:
            line_up = line.upper()
            if not any(word in line_up for word in noise) and 3 < len(line.split()) < 6:
                clean = re.sub(r'[^a-zA-Z\s]', '', line).strip().upper()
                if clean not in found:
                    found.append(clean)

    # 5. Final Law Detection (more inclusive)
    # Using a set to ensure unique laws only
    law_patterns = r'(Section\s\d+|Maintenance|CrPC|HMA|DV\sAct|Custody|Domestic\sViolence)'
    laws_found = list(set(re.findall(law_patterns, text, re.I)))

    return {
        "Parties": [found[0] if len(found) > 0 else "Not detected", 
                    found[1] if len(found) > 1 else "Not detected"],
        "Laws": laws_found
    }}

def extract_timeline(text):
    # This finds any date like February 14, 2023 or 14/02/2023
    date_regex = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}[\s,]+\d{4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    found = re.findall(date_regex, text, re.I)
    unique = list(dict.fromkeys([d.strip() for d in found]))
    return [f"Key Date: {d}" for d in unique[:6]] if unique else ["No dates found"] parties name not detected , correct the code

    






































