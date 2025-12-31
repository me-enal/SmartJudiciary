import re

def find_legal_details(text):
    # Safety check: Is the PDF even readable?
    if not text or len(text.strip()) < 10:
        return {"Parties": ["PDF UNREADABLE", "POSSIBLY AN IMAGE SCAN"], "Laws": ["No text detected"]}

    details = {"Parties": [], "Laws": []}
    
    # 1. Get the first 15 lines that are not empty
    lines = [l.strip() for l in text[:3000].split('\n') if len(l.strip()) > 3]
    
    # 2. BRUTE FORCE: Just grab the first few lines that look like names
    # We skip lines that are clearly just "High Court" or "Judgment"
    ignore_list = ["COURT", "JUDGE", "BENCH", "ORDER", "JUDGMENT", "DATED", "ADVOCATE", "NO", "YEAR"]
    
    potential = []
    for line in lines:
        # If the line contains a name in brackets (Anjali Sharma), prioritize it
        bracket_match = re.search(r'\(([^)]+)\)', line)
        if bracket_match:
            potential.append(bracket_match.group(1).upper())
        
        # Otherwise, if it's a short line and not 'noise', add it
        elif not any(word in line.upper() for word in ignore_list) and len(line.split()) < 6:
            # Clean off the legal titles like Smt/Shri
            clean = re.sub(r'\b(SMT|SHRI|MR|MS|MRS|THE|APPELLANT|RESPONDENT|PETITIONER)\b', '', line, flags=re.I)
            clean = re.sub(r'[^a-zA-Z\s]', '', clean).strip()
            if len(clean) > 2:
                potential.append(clean.upper())

    # 3. Take the first two unique items found
    unique_candidates = []
    for p in potential:
        if p not in unique_candidates:
            unique_candidates.append(p)

    if len(unique_candidates) >= 2:
        details["Parties"] = [unique_candidates[0], unique_candidates[1]]
    elif len(unique_candidates) == 1:
        details["Parties"] = [unique_candidates[0], "RESPONDENT NOT FOUND"]
    else:
        # ABSOLUTE FALLBACK: Just give the first two lines of the PDF
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































