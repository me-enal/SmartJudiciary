import re

def find_legal_details(text):
    details = {"Parties": [], "Laws": []}
    
    # 1. LIMIT TO THE FIRST 1500 CHARACTERS (The Title Page)
    # This prevents the AI from looking at the middle of the judgment
    header = text[:1500]
    lines = [line.strip() for line in header.split('\n') if len(line.strip()) > 2]

    p1, p2 = "Not detected", "Not detected"

    # 2. VERTICAL SEARCH WITH SENTENCE BLOCKER
    for i, line in enumerate(lines):
        # Find 'Appellant' label
        if re.search(r'\b(Appellant|Petitioner|Applicant)\b', line, re.I):
            # Look at the 2 lines ABOVE the label
            for j in range(i-1, max(-1, i-3), -1):
                name_candidate = lines[j].strip()
                # A name is usually 1-4 words. If it's a long sentence, it's NOT a name.
                if 1 <= len(name_candidate.split()) <= 5:
                    if not re.search(r'(COURT|JUDGE|ORDER|DATED|DATE)', name_candidate, re.I):
                        p1 = name_candidate
                        break
        
        # Find 'Respondent' label
        if re.search(r'\b(Respondent|Defendant)\b', line, re.I):
            for k in range(i-1, max(-1, i-3), -1):
                name_candidate = lines[k].strip()
                if 1 <= len(name_candidate.split()) <= 5:
                    if not re.search(r'(VERSUS|VS|V/S|AGAINST)', name_candidate, re.I):
                        p2 = name_candidate
                        break

    # 3. CLEANING NOISE
    # Remove "The", "Smt", "Shri", and extra dots/numbers
    def clean_name(name):
        name = re.sub(r'^(THE|SMT|SHRI|MR|MS|MRS|MD)\.?\s+', '', name, flags=re.I)
        name = re.sub(r'[\d\.…]+', '', name) # Remove numbers and dots
        return name.strip().upper()

    details["Parties"] = [clean_name(p1), clean_name(p2)]

    # 4. LAW DETECTION (Stable)
    law_keywords = ["Section 125", "CrPC", "Maintenance", "Custody", "Hindu Marriage Act"]
    for law in law_keywords:
        if re.search(r'\b' + re.escape(law) + r'\b', text, re.I):
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    # This captures dates specifically formatted in Indian judgments
    date_regex = r'(\d{1,2}(?:st|nd|rd|th)?[\s\.\-/]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]*\d{2,4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    matches = re.findall(date_regex, text, re.I)
    unique_dates = list(dict.fromkeys([m.strip() for m in matches]))
    return [f"Key Date: {d}" for d in unique_dates[:8]]













