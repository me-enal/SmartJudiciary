import re

def find_legal_details(text):
    # 1. Check if there is ANY text at all
    if not text or len(text.strip()) < 10:
        return {"Parties": ["PDF IS A SCAN/IMAGE", "CANNOT READ TEXT"], "Laws": ["Use a searchable PDF"]}

    details = {"Parties": ["Not detected", "Not detected"], "Laws": []}
    
    # 2. Get the first 10 lines that aren't empty
    lines = [l.strip() for l in text[:2000].split('\n') if len(l.strip()) > 2]
    
    # 3. ABSOLUTE BRUTE FORCE
    # We ignore headers and just take the first two 'clean' lines
    noise = ["COURT", "JUDGE", "BENCH", "ORDER", "JUDGMENT", "DATED", "NO.", "YEAR", "VERSUS", "VS"]
    
    candidates = []
    for line in lines:
        # If the line has brackets like (Anjali Sharma), it's our winner
        bracket_match = re.search(r'\(([^)]+)\)', line)
        if bracket_match:
            candidates.append(bracket_match.group(1).upper())
            continue
            
        # Otherwise, take short lines that aren't noise
        if not any(word in line.upper() for word in noise) and len(line.split()) < 6:
            clean = re.sub(r'\b(SMT|SHRI|MR|MS|MRS|THE|APPELLANT|RESPONDENT|PETITIONER)\b', '', line, flags=re.I)
            clean = re.sub(r'[^a-zA-Z\s]', '', clean).strip()
            if len(clean) > 2:
                candidates.append(clean.upper())

    # 4. Fill the parties list
    if len(candidates) >= 2:
        details["Parties"] = [candidates[0], candidates[1]]
    elif len(candidates) == 1:
        details["Parties"] = [candidates[0], "Check Respondent Manually"]
    else:
        # LAST RESORT: Just show the first two lines of the file no matter what
        details["Parties"] = [lines[0][:30] if len(lines) > 0 else "Empty", 
                              lines[1][:30] if len(lines) > 1 else "Empty"]

    # 5. LAW DETECTION
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
































