import re

def find_legal_details(text):
    if not text or len(text.strip()) < 10:
        return {"Parties": ["Not detected", "Not detected"], "Laws": []}

    details = {"Parties": ["Not detected", "Not detected"], "Laws": []}
    lines = [l.strip() for l in text[:3000].split('\n') if len(l.strip()) > 2]

    p1, p2 = "Not detected", "Not detected"

    for line in lines:
        line_up = line.upper()
        
        # 1. Look for Petitioner/Appellant
        if ("APPELLANT" in line_up or "PETITIONER" in line_up) and p1 == "Not detected":
            clean = re.sub(r'\b(APPELLANT|PETITIONER|THE|SMT|SHRI|MR|MS|MRS)\b', '', line, flags=re.I)
            p1 = re.sub(r'[^a-zA-Z\s]', '', clean).strip().upper()
            continue 

        # 2. Look for Respondent
        if ("RESPONDENT" in line_up or "DEFENDANT" in line_up) and p2 == "Not detected":
            clean = re.sub(r'\b(RESPONDENT|DEFENDANT|THE|SMT|SHRI|MR|MS|MRS)\b', '', line, flags=re.I)
            p2 = re.sub(r'[^a-zA-Z\s]', '', clean).strip().upper()

    # 3. Handle the 'Versus' Case fallback
    if p2 == "Not detected":
        for i, line in enumerate(lines):
            if "VERSUS" in line.upper() or " VS " in line.upper():
                if i + 1 < len(lines):
                    p2 = re.sub(r'[^a-zA-Z\s]', '', lines[i+1]).strip().upper()

    details["Parties"] = [p1, p2]

    # 4. Law Finder
    laws = ["Section 125", "Maintenance", "CrPC", "HMA", "Custody"]
    for law in laws:
        if law.lower() in text.lower():
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    # This function is needed because your app.py tries to import it on line 14
    date_regex = r'(\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}[\s,]+\d{4})'
    found = re.findall(date_regex, text, re.I)
    unique = list(dict.fromkeys(found))
    return [f"Date: {d}" for d in unique[:5]] if unique else ["No dates found"]

    









































