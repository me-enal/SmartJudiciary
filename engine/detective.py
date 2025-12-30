import re

def find_legal_details(text):
    details = {"Parties": ["Not detected", "Not detected"], "Laws": []}
    
    # 1. Focus on the header (First 3000 chars)
    header = text[:3000]
    
    # 2. THE "FORBIDDEN" LIST
    # If the code finds these words, it will REJECT them as names.
    forbidden = {
        "INCOME", "ASSETS", "EXPENDITURE", "LIABILITIES", "MONTHLY", 
        "AFFIDAVIT", "ORDER", "JUDGMENT", "COURT", "DELHI", "HIGH", 
        "VERSUS", "VS", "V/S", "PETITION", "APPEAL", "MAINTENANCE",
        "SECTION", "CRPC", "IPC", "HMA", "DATED", "JURISDICTION"
    }

    # 3. VERTICAL SEARCH STRATEGY
    # We look for the names line-by-line near the 'VERSUS' anchor
    lines = [l.strip() for l in header.split('\n') if len(l.strip()) > 2]
    
    for i, line in enumerate(lines):
        if re.search(r'\b(VERSUS|VS|V/S)\b', line, re.I):
            # Look UP for Petitioner (The 3 lines above VERSUS)
            for j in range(i-1, max(-1, i-4), -1):
                cand = lines[j].upper()
                # If the line isn't in our forbidden list and isn't a sentence
                if not any(word in cand for word in forbidden) and len(cand.split()) < 5:
                    details["Parties"][0] = re.sub(r'[^A-Z\s]', '', cand).strip()
                    break
            
            # Look DOWN for Respondent (The 3 lines below VERSUS)
            for k in range(i+1, min(len(lines), i+4)):
                cand = lines[k].upper()
                if not any(word in cand for word in forbidden) and len(cand.split()) < 5:
                    details["Parties"][1] = re.sub(r'[^A-Z\s]', '', cand).strip()
                    break

    # 4. LAW DETECTION
    law_map = {
        "Section 125": r"125\s+Cr\.?P\.?C",
        "Maintenance": r"Maintenance",
        "Custody": r"Custody",
        "Hindu Marriage Act": r"Hindu\s+Marriage\s+Act",
        "Domestic Violence": r"Domestic\s+Violence"
    }
    for law, pattern in law_map.items():
        if re.search(pattern, text, re.I):
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    # This regex captures 14.10.2023, 14th Oct 2023, and Oct 14, 2023
    date_pattern = r'(\d{1,2}(?:st|nd|rd|th)?[\s\.\-/]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]*\d{2,4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    
    matches = re.findall(date_pattern, text, re.I)
    # Remove duplicates and return first 5 dates
    seen = set()
    unique_dates = [x for x in matches if not (x in seen or seen.add(x))]
    
    return [f"Event Date: {d}" for d in unique_dates[:6]] if unique_dates else ["No dates found"]


















