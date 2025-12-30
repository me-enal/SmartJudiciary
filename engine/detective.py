import re

def find_legal_details(text):
    details = {"Parties": [], "Laws": []}
    
    # 1. Focus on the Title Page (First 2500 characters)
    header = text[:2500]
    
    # 2. Pre-Clean the text: Remove dots and fix spacing
    header = re.sub(r'\.{2,}', ' ', header)
    header = ' '.join(header.split())

    # 3. BLACKLIST: Words that are NOT names but often appear in caps
    blacklist = [
        "INCOME", "JUDGMENT", "ORDER", "COURT", "MATRIMONIAL", 
        "JURISDICTION", "DATE", "OFFICE", "ADVOCATE", "SECTION",
        "APPEAL", "MAINTENANCE", "PETITION", "REVISION", "AFFIDAVIT"
    ]

    p1, p2 = "Not detected", "Not detected"

    # 4. SEARCH STRATEGY: Look for the VERSUS anchor
    vs_pattern = r"(.*?)\s+(?:VERSUS|V/S|VS\.?)\s+(.*)"
    vs_match = re.search(vs_pattern, header, re.IGNORECASE)

    if vs_match:
        # Get 4 words before and after VS
        before_vs = vs_match.group(1).split()[-4:]
        after_vs = vs_match.group(2).split()[:4]
        
        # Filter out blacklisted words
        clean_p1 = [w for w in before_vs if w.upper() not in blacklist]
        clean_p2 = [w for w in after_vs if w.upper() not in blacklist]
        
        p1 = ' '.join(clean_p1)
        p2 = ' '.join(clean_p2)

    # 5. FINAL POLISH
    def final_clean(name):
        # Remove common prefixes/titles
        name = re.sub(r'\b(SMT|SHRI|MR|MS|MRS|THE|APPELLANT|RESPONDENT|PETITIONER)\b', '', name, flags=re.I)
        # Remove anything that isn't a letter
        name = re.sub(r'[^a-zA-Z\s]', '', name)
        return name.strip().upper()

    details["Parties"] = [final_clean(p1), final_clean(p2)]

    # 6. LAW DETECTION (Stable)
    law_keywords = ["Section 125", "CrPC", "Maintenance", "Custody", "Hindu Marriage Act"]
    for law in law_keywords:
        if re.search(r'\b' + re.escape(law) + r'\b', text, re.I):
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    # Regex for Indian dates like 14.10.2023 or 14th Oct 2023
    date_regex = r'(\d{1,2}(?:st|nd|rd|th)?[\s\.\-/]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]*\d{2,4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    matches = re.findall(date_regex, text, re.I)
    unique_dates = list(dict.fromkeys([m.strip() for m in matches]))
    return [f"Key Date: {d}" for d in unique_dates[:8]]















