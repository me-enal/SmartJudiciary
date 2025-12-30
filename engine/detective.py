import re

def find_legal_details(text):
    details = {"Parties": [], "Laws": []}
    
    # Split text into lines to analyze structure
    lines = [line.strip() for line in text[:4000].split('\n') if line.strip()]

    p1, p2 = "Not detected", "Not detected"

    # --- 1. VERTICAL SEARCH FOR PARTIES ---
    for i, line in enumerate(lines):
        # Look for the word 'Appellant' or 'Petitioner'
        if re.search(r'\b(Appellant|Petitioner|Applicant|Plaintiff)\b', line, re.I):
            # The name is usually 1 or 2 lines ABOVE this label
            for j in range(i-1, max(-1, i-3), -1):
                potential_name = lines[j].replace('.', '').strip()
                if len(potential_name) > 3 and not re.search(r'(COURT|JUDICIAL|ADVOCATE|HONBLE)', potential_name, re.I):
                    p1 = potential_name
                    break
        
        # Look for the word 'Respondent' or 'Defendant'
        if re.search(r'\b(Respondent|Defendant)\b', line, re.I):
            # The name is usually 1 or 2 lines ABOVE this label
            for k in range(i-1, max(-1, i-3), -1):
                potential_name = lines[k].replace('.', '').strip()
                if len(potential_name) > 3 and not re.search(r'(VERSUS|VS|V/S)', potential_name, re.I):
                    p2 = potential_name
                    break

    # --- 2. CLEANUP NOISE ---
    # Remove common prefix/suffix noise
    noise_patterns = [r'^THE\s+', r'\.\.\.', r'\d+', r'\(.*?\)', r'MR\s+', r'MS\s+', r'SMT\s+']
    for pattern in noise_patterns:
        p1 = re.sub(pattern, '', p1, flags=re.I).strip()
        p2 = re.sub(pattern, '', p2, flags=re.I).strip()

    details["Parties"] = [p1.upper(), p2.upper()]

    # --- 3. LAW DETECTION (Stable) ---
    law_keywords = ["Section 125", "CrPC", "Maintenance", "Custody", "Hindu Marriage Act"]
    for law in law_keywords:
        if re.search(r'\b' + re.escape(law) + r'\b', text, re.I):
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    # Expanded to catch "October 14, 2023" specifically
    date_regex = r'(\d{1,2}(?:st|nd|rd|th)?[\s\.\-/]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]*\d{2,4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    matches = re.findall(date_regex, text, re.I)
    unique_dates = list(dict.fromkeys([m.strip() for m in matches]))
    return [f"Key Date: {d}" for d in unique_dates[:8]]












