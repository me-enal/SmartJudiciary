import re

def find_legal_details(text):
    details = {"Parties": ["Not detected", "Not detected"], "Laws": []}
    
    # 1. Focus on the header
    header = text[:3000]
    lines = [l.strip() for l in header.split('\n') if len(l.strip()) > 2]

    p1, p2 = "Not detected", "Not detected"

    # 2. THE PRECISION SCANNER
    for i, line in enumerate(lines):
        # Scan for Petitioner/Appellant
        if any(word in line.upper() for word in ["APPELLANT", "PETITIONER", "PLAINTIFF"]):
            # CROP: Take the line, but stop if you see these words
            clean = re.split(r'\(|alleges|was|forced|challenged|filed|is\b', line, flags=re.I)[0]
            p1 = clean.replace('the', '').replace('The', '').strip()
        
        # Scan for Respondent/Defendant
        if any(word in line.upper() for word in ["RESPONDENT", "DEFENDANT"]):
            # CROP: Stop before the argument starts
            clean = re.split(r'\(|challenged|arguing|denies|states|is\b', line, flags=re.I)[0]
            p2 = clean.replace('the', '').replace('The', '').strip()

    # 3. CLEAN UP BRACKETS AND TITLES
    def final_fix(name):
        name = re.sub(r'[^a-zA-Z\s]', '', name) # Remove numbers/dots
        return name.strip().upper()

    details["Parties"] = [final_fix(p1), final_fix(p2)]

    # 4. LAW DETECTION
    for law in ["Section 125", "Maintenance", "Hindu Marriage Act", "Custody", "CrPC"]:
        if re.search(r'\b' + re.escape(law) + r'\b', text, re.I):
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    # Improved Date Finder: Catches "September 15, 2020" and "15.09.2020"
    date_regex = r'(\d{1,2}(?:st|nd|rd|th)?[\s\.\-/]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]*\d{2,4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4}|(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}[\s,]+\d{4})'
    
    found = re.findall(date_regex, text, re.I)
    unique_dates = list(dict.fromkeys([d.strip() for d in found]))
    
    return [f"Key Date: {d}" for d in unique_dates[:8]] if unique_dates else ["No specific dates found"]





















