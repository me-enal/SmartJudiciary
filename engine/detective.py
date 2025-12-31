import re

def find_legal_details(text):
    details = {"Parties": ["Not detected", "Not detected"], "Laws": []}
    
    # 1. Check if the PDF is actually readable
    if not text or len(text.strip()) < 10:
        return {"Parties": ["PDF UNREADABLE", "POSSIBLY A SCAN"], "Laws": ["Try a different PDF"]}

    # 2. Get the first 15 lines of text
    lines = [l.strip() for l in text[:2500].split('\n') if len(l.strip()) > 2]
    
    # 3. THE VACUUM: Collect anything that looks like a name
    # We ignore lines with these "Bad Words"
    bad_words = ["COURT", "JUDGE", "DATE", "ORDER", "JUDGMENT", "ADVOCATE", "STREET", "ROAD", "VERSUS", "VS", "V/S"]
    
    candidates = []
    for line in lines:
        # Priority: If it's in brackets (Anjali Sharma), it's definitely a name
        bracket_match = re.search(r'\(([^)]+)\)', line)
        if bracket_match:
            name = bracket_match.group(1)
            candidates.append(name.strip().upper())
            continue
            
        # Fallback: If the line is short (1-4 words) and not in the bad_words list
        if not any(word in line.upper() for word in bad_words) and len(line.split()) < 5:
            # Remove legal titles
            clean = re.sub(r'\b(SMT|SHRI|MR|MS|MRS|THE|APPELLANT|RESPONDENT|PETITIONER)\b', '', line, flags=re.I)
            clean = re.sub(r'[^a-zA-Z\s]', '', clean).strip()
            if len(clean) > 2:
                candidates.append(clean.upper())

    # 4. Pick the first two unique names found
    final_list = []
    for c in candidates:
        if c not in final_list:
            final_list.append(c)
            
    if len(final_list) >= 2:
        details["Parties"] = [final_list[0], final_list[1]]
    elif len(final_list) == 1:
        details["Parties"] = [final_list[0], "Check Respondent Manually"]

    # 5. LAW DETECTION
    law_map = ["Section 125", "Maintenance", "Hindu Marriage Act", "Custody", "CrPC", "HMA"]
    for law in law_map:
        if law.lower() in text.lower():
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    # This finds any date like February 14, 2023 or 14/02/2023
    date_regex = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}[\s,]+\d{4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    found = re.findall(date_regex, text, re.I)
    unique = list(dict.fromkeys([d.strip() for d in found]))
    return [f"Key Date: {d}" for d in unique[:6]] if unique else ["No dates found"]






























