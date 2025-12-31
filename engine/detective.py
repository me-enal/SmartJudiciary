import re

def find_legal_details(text):
    # Safety check: Is the PDF readable?
    if not text or len(text.strip()) < 10:
        return {"Parties": ["PDF UNREADABLE", "POSSIBLY A SCAN"], "Laws": ["Try a different PDF"]}

    details = {"Parties": ["Not detected", "Not detected"], "Laws": []}
    
    # 1. Clean the header and get first 20 lines
    lines = [l.strip() for l in text[:3000].split('\n') if len(l.strip()) > 2]
    
    # 2. Blacklist of words that are definitely NOT names
    blacklist = ["COURT", "JUDGE", "BENCH", "ORDER", "JUDGMENT", "DATED", "ADVOCATE", "NO", "YEAR", "VERSUS", "VS", "V/S"]

    potential_names = []
    for line in lines:
        # Priority: If it's in brackets like (Anjali Sharma), it's the name
        bracket_match = re.search(r'\(([^)]+)\)', line)
        if bracket_match:
            candidate = bracket_match.group(1).strip()
            # Ignore if bracket just says (Appellant)
            if not any(x in candidate.upper() for x in ["APPELLANT", "RESPONDENT", "PETITIONER"]):
                potential_names.append(candidate.upper())
                continue
        
        # Fallback: Short lines at the top that aren't 'noise'
        if not any(word in line.upper() for word in blacklist) and len(line.split()) < 6:
            # Remove legal titles
            clean = re.sub(r'\b(SMT|SHRI|MR|MS|MRS|THE|APPELLANT|RESPONDENT|PETITIONER|DEFENDANT)\b', '', line, flags=re.I)
            clean = re.sub(r'[^a-zA-Z\s]', '', clean).strip()
            if len(clean) > 3:
                potential_names.append(clean.upper())

    # 3. Pick the first two unique names
    unique_names = []
    for n in potential_names:
        if n not in unique_names:
            unique_names.append(n)

    if len(unique_names) >= 2:
        details["Parties"] = [unique_names[0], unique_names[1]]
    elif len(unique_names) == 1:
        details["Parties"] = [unique_names[0], "RESPONDENT NOT FOUND"]
    else:
        # ABSOLUTE FALLBACK: Just give the first two text lines
        details["Parties"] = [lines[0][:30] if len(lines) > 0 else "Empty", 
                              lines[1][:30] if len(lines) > 1 else "Empty"]

    # 4. LAW DETECTION
    for law in ["Section 125", "Maintenance", "Hindu Marriage Act", "CrPC", "HMA"]:
        if law.lower() in text.lower():
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    # This finds any date like February 14, 2023 or 14/02/2023
    date_regex = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}[\s,]+\d{4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    found = re.findall(date_regex, text, re.I)
    unique = list(dict.fromkeys([d.strip() for d in found]))
    return [f"Key Date: {d}" for d in unique[:6]] if unique else ["No dates found"]

































