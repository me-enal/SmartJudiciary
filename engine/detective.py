import re

def find_legal_details(text):
    details = {"Parties": [], "Laws": []}
    
    # 1. Focus on the first 2000 characters only
    header = text[:2000]
    
    # 2. Clean the noise (remove dots and standardize spaces)
    header = re.sub(r'\.{2,}', ' ', header)
    header = ' '.join(header.split())

    p1, p2 = "Not detected", "Not detected"

    # 3. STRATEGY: Find the 'VERSUS' anchor
    # This is the most reliable way to find names in High Court documents
    vs_match = re.search(r'(.*?)\s+(?:VERSUS|V/S|VS\.?)\s+(.*)', header, re.IGNORECASE)

    if vs_match:
        cand1 = vs_match.group(1).strip()
        cand2 = vs_match.group(2).strip()

        # Split into words and take only the last few words before VS and first few after
        # This prevents grabbing long sentences
        words1 = cand1.split()
        words2 = cand2.split()

        # Names are usually 2-4 words long
        p1 = ' '.join(words1[-4:]) if len(words1) > 0 else "Not detected"
        p2 = ' '.join(words2[:4]) if len(words2) > 0 else "Not detected"

    # 4. FINAL CLEANUP: Remove titles and legal labels
    def clean_final(name):
        # Remove labels like Appellant, Respondent, etc.
        name = re.sub(r'(APPELLANT|RESPONDENT|PETITIONER|SMT|SHRI|MR|MS|THE)\.?\b', '', name, flags=re.I)
        # Remove numbers and special characters
        name = re.sub(r'[^a-zA-Z\s]', '', name)
        return name.strip().upper()

    details["Parties"] = [clean_final(p1), clean_final(p2)]

    # 5. LAW DETECTION (Stable)
    law_keywords = ["Section 125", "CrPC", "Maintenance", "Custody", "Hindu Marriage Act"]
    for law in law_keywords:
        if re.search(r'\b' + re.escape(law) + r'\b', text, re.I):
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    # Catches 14.10.2023 or October 14, 2023
    date_regex = r'(\d{1,2}(?:st|nd|rd|th)?[\s\.\-/]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]*\d{2,4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    matches = re.findall(date_regex, text, re.I)
    unique_dates = list(dict.fromkeys([m.strip() for m in matches]))
    return [f"Key Date: {d}" for d in unique_dates[:8]]














