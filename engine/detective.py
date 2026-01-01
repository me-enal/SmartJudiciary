import re

def find_legal_details(text):
    # 1. Basic check
    if not text or len(text.strip()) < 10:
        return {"Parties": ["Not detected", "Not detected"], "Laws": []}

    details = {"Parties": ["Not detected", "Not detected"], "Laws": []}
    
    # 2. Get the header lines
    lines = [l.strip() for l in text[:3000].split('\n') if len(l.strip()) > 2]

    p1, p2 = "Not detected", "Not detected"

    # 3. Simple Keyword Scan (The "First Code" Logic)
    for line in lines:
        line_up = line.upper()
        
        # If the line mentions Petitioner/Appellant, take the whole line
        if "APPELLANT" in line_up or "PETITIONER" in line_up:
            if p1 == "Not detected":
                # Clean only the legal labels, keep the rest
                p1 = re.sub(r'\b(APPELLANT|PETITIONER|THE|SMT|SHRI|MR|MS|MRS)\b', '', line, flags=re.I)
                p1 = re.sub(r'[^a-zA-Z\s]', '', p1).strip().upper()

        # If the line mentions Respondent, take the whole line
        if "RESPONDENT" in line_up or "DEFENDANT" in line_up:
            if p2 == "Not detected":
                p2 = re.sub(r'\b(RESPONDENT|DEFENDANT|THE|SMT|SHRI|MR|MS|MRS)\b', '', line, flags=re.I)
                p2 = re.sub(r'[^a-zA-Z\s]', '', p2).strip().upper()

    details["Parties"] = [p1, p2]

    # 4. Simple Law Finder
    laws = ["Section 125", "Maintenance", "CrPC", "HMA", "Custody"]
    for law in laws:
        if law.lower() in text.lower():
            details["Laws"].append(law)
            
    return details

    








































