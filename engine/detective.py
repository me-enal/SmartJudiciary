import re

def find_legal_details(text):
    details = {"Parties": [], "Laws": []}
    
    # 1. Focus strictly on the first 2500 characters
    header = text[:2500]
    
    # 2. Clean noise: Remove dots, multiple spaces, and lines
    header = re.sub(r'\.{2,}', ' ', header)
    header = re.sub(r'\s+', ' ', header)

    # 3. THE "NEVER-A-NAME" BLACKLIST
    # This ensures common financial/legal terms are never picked as names
    legal_terms = {
        "INCOME", "ASSETS", "EXPENDITURE", "MONTHLY", "ORDER", "JUDGMENT", 
        "COURT", "MATRIMONIAL", "APPEAL", "JURISDICTION", "DATE", "OFFICE", 
        "ADVOCATE", "SECTION", "MAINTENANCE", "PETITION", "REVISION", 
        "AFFIDAVIT", "VERSUS", "VS", "V/S", "HIGH", "DELHI", "BENCH", 
        "HONBLE", "JUSTICE", "CRPC", "IPC", "HMA", "FAMILY", "CASE", "NO",
        "YEAR", "DATED", "BETWEEN", "AND", "OTHERS", "ORS", "ANR", "ANOTHER"
    }

    p1, p2 = "Not detected", "Not detected"

    # 4. SEARCH STRATEGY: Center-out from VERSUS
    vs_match = re.search(r"(.*?)\s+(?:VERSUS|V/S|VS\.?)\s+(.*)", header, re.IGNORECASE)

    if vs_match:
        # Get words before and after VS
        before_vs = vs_match.group(1).split()
        after_vs = vs_match.group(2).split()
        
        # Grab the 6 words closest to VERSUS
        # We filter out any word that is in our legal_terms list
        clean_p1 = [w for w in before_vs[-6:] if w.upper().strip(',.') not in legal_terms]
        clean_p2 = [w for w in after_vs[:6] if w.upper().strip(',.') not in legal_terms]
        
        # Remove common titles like SMT, SHRI, MR
        titles = {"SMT", "SHRI", "MR", "MS", "MRS", "THE", "APPELLANT", "RESPONDENT", "PETITIONER"}
        final_p1 = [w for w in clean_p1 if w.upper().strip(',.') not in titles]
        final_p2 = [w for w in clean_p2 if w.upper().strip(',.') not in titles]
        
        p1 = ' '.join(final_p1)
        p2 = ' '.join(final_p2)

    # 5. FINAL CLEANUP: Remove numbers and symbols
    def final_polish(name):
        name = re.sub(r'[^a-zA-Z\s]', '', name)
        return name.strip().upper()

    details["Parties"] = [final_polish(p1) or "Not detected", final_polish(p2) or "Not detected"]

    # 6. LAW DETECTION (Stable)
    law_keywords = ["Section 125", "CrPC", "Maintenance", "Custody", "Hindu Marriage Act", "HMA"]
    for law in law_keywords:
        if re.search(r'\b' + re.escape(law) + r'\b', text, re.I):
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    # Enhanced regex to catch dates like "October 14, 2023" or "14.10.2023"
    date_regex = r'(\d{1,2}(?:st|nd|rd|th)?[\s\.\-/]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]*\d{2,4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4}|(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}[\s,]+\d{4})'
    matches = re.findall(date_regex, text, re.I)
    unique_dates = list(dict.fromkeys([m.strip() for m in matches]))
    return [f"Key Date: {d}" for d in unique_dates[:8]]

















