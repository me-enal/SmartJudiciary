import re

def find_legal_details(text):
    details = {"Parties": ["Not detected", "Not detected"], "Laws": []}
    
    # 1. Look ONLY at the first 1500 characters (The Header)
    # This prevents the AI from reading the 'Architect' part in the body
    header = text[:1500]
    lines = [l.strip() for l in header.split('\n') if len(l.strip()) > 2]

    # 2. Find the 'VERSUS' line as our anchor
    vs_idx = -1
    for i, line in enumerate(lines):
        if re.search(r'\b(VERSUS|V/S|VS)\b', line, re.I):
            vs_idx = i
            break
    
    # 3. Extract names based on the VS anchor
    if vs_idx != -1:
        # Petitioner is above VS
        raw_p1 = lines[vs_idx - 1] if vs_idx > 0 else "Not detected"
        # Respondent is below VS
        raw_p2 = lines[vs_idx + 1] if vs_idx < len(lines) - 1 else "Not detected"
        
        # Clean the names (Look for brackets first)
        def extract_name(text_line):
            # If name is in brackets like (Anjali Sharma), take that
            bracket_match = re.search(r'\(([^)]+)\)', text_line)
            if bracket_match:
                return bracket_match.group(1)
            # Otherwise, remove legal titles
            clean = re.sub(r'\b(THE|APPELLANT|RESPONDENT|PETITIONER|SMT|SHRI|MR|MS|MRS)\b', '', text_line, flags=re.I)
            clean = re.sub(r'[^a-zA-Z\s]', '', clean)
            return clean.strip()

        details["Parties"] = [extract_name(raw_p1).upper(), extract_name(raw_p2).upper()]

    # 4. LAW DETECTION
    law_keywords = ["Section 125", "Maintenance", "Hindu Marriage Act", "Custody", "CrPC"]
    for law in law_keywords:
        if re.search(r'\b' + re.escape(law) + r'\b', text, re.I):
            details["Laws"].append(law)
            
    return details


def extract_timeline(text):
    # This pattern specifically looks for Month Day, Year (September 15, 2020)
    # and DD.MM.YYYY
    date_pattern = r'((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}[\s,]+\d{4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    
    found = re.findall(date_pattern, text, re.I)
    # Clean duplicates
    unique_dates = []
    for d in found:
        if d not in unique_dates:
            unique_dates.append(d)
            
    return [f"Event: {d}" for d in unique_dates[:8]] if unique_dates else ["No specific dates found"]

























