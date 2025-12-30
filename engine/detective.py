import re

def find_legal_details(text):
    details = {"Parties": [], "Laws": []}
    
    # 1. Focus on the Title Page (First 2000 characters)
    header = text[:2000]
    
    # 2. Pre-Clean: Remove long dots and standardize whitespace
    header = re.sub(r'\.{2,}', ' ', header)
    header = ' '.join(header.split())

    # 3. BLACKLIST: Words to NEVER treat as names
    blacklist = [
        "INCOME", "JUDGMENT", "ORDER", "COURT", "MATRIMONIAL", "APPEAL",
        "JURISDICTION", "DATE", "OFFICE", "ADVOCATE", "SECTION", "VS",
        "MAINTENANCE", "PETITION", "REVISION", "AFFIDAVIT", "VERSUS",
        "HIGH", "DELHI", "BENCH", "HONBLE", "JUSTICE", "CRPC", "IPC"
    ]

    p1, p2 = "Not detected", "Not detected"

    # 4. SEARCH STRATEGY: Center-out from "VERSUS"
    # This finds the 'VERSUS' anchor and looks at 5 words on each side
    vs_match = re.search(r"(.*?)\s+(?:VERSUS|V/S|VS\.?)\s+(.*)", header, re.IGNORECASE)

    if vs_match:
        # Split text into individual words
        before_vs = vs_match.group(1).split()
        after_vs = vs_match.group(2).split()
        
        # Take the 5 words closest to 'VERSUS'
        near_p1 = before_vs[-5:] if len(before_vs) > 0 else []
        near_p2 = after_vs[:5] if len(after_vs) > 0 else []
        
        # Filter out blacklisted words and common titles
        titles = ["SMT", "SHRI", "MR", "MS", "MRS", "THE", "APPELLANT", "RESPONDENT", "PETITIONER"]
        
        clean_p1 = [w for w in near_p1 if w.upper() not in blacklist and w.upper() not in titles]
        clean_p2 = [w for w in near_p2 if w.upper() not in blacklist and w.upper() not in titles]
        
        p1 = ' '.join(clean_p1)
        p2 = ' '.join(clean_p2)

    # 5. FINAL POLISH
    def final_clean(name):
        # Remove numbers and special characters like commas or brackets
        name = re.sub(r'[^a-zA-Z\s]', '', name)
        return name.strip().upper()

    details["Parties"] = [final_clean(p1), final_clean(p2)]

    # 6. LAW DETECTION
    law_keywords = ["Section 125", "CrPC", "Maintenance", "Custody", "Hindu Marriage Act"]
    for law in law_keywords:
        if re.search(r'\b' + re.escape(law) + r'\b', text, re.I):
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    # Advanced date parser for Indian formats
    date_regex = r'(\d{1,2}(?:st|nd|rd|th)?[\s\.\-/]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]*\d{2,4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    matches = re.findall(date_regex, text, re.I)
    unique_dates = list(dict.fromkeys([m.strip() for m in matches]))
    return [f"Key Date: {d}" for d in unique_dates[:8]]
















