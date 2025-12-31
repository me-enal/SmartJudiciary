import re

def find_legal_details(text):
    details = {"Parties": ["Not detected", "Not detected"], "Laws": []}
    
    # 1. Focus only on the very top of the document (The Header)
    # This prevents the code from 'wandering' into the 'Architect' section
    header = text[:1500]
    
    # 2. Look for the VERSUS anchor
    # We look for Petitioner [VERSUS] Respondent
    vs_match = re.search(r"(.*?)\s+(?:VERSUS|V/S|VS\.?)\s+(.*)", header, re.IGNORECASE)

    if vs_match:
        # Get the text immediately before and after VERSUS
        raw_p1 = vs_match.group(1).strip()
        raw_p2 = vs_match.group(2).strip()

        # 3. THE NAME EXTRACTOR
        def isolate_name(raw_text, side="left"):
            # If there's a name in brackets like (Anjali Sharma), take it
            brackets = re.findall(r'\(([^)]+)\)', raw_text)
            if brackets:
                return brackets[-1] # Take the last bracketed text
            
            # If no brackets, take the last 3 words (if left side) or first 3 (if right side)
            words = raw_text.split()
            if side == "left":
                return " ".join(words[-3:]) if words else "Not detected"
            else:
                return " ".join(words[:3]) if words else "Not detected"

        p1 = isolate_name(raw_p1, "left")
        p2 = isolate_name(raw_p2, "right")

        # 4. FINAL CLEANUP (Remove 'Appellant', 'Respondent', and 'Architect' noise)
        def clean(name):
            name = re.sub(r'\b(THE|APPELLANT|RESPONDENT|PETITIONER|SMT|SHRI|MR|MS|MRS|ARCHITECT|COURT|FINDS|HOWEVER)\b', '', name, flags=re.I)
            name = re.sub(r'[^a-zA-Z\s]', '', name)
            return name.strip().upper()

        details["Parties"] = [clean(p1), clean(p2)]

    # 5. LAW DETECTION
    laws = ["Section 125", "Maintenance", "Hindu Marriage Act", "Custody", "CrPC"]
    for law in laws:
        if re.search(r'\b' + re.escape(law) + r'\b', text, re.I):
            details["Laws"].append(law)
            
    return details



def extract_timeline(text):
    # This pattern specifically looks for Month Day, Year (September 15, 2020)
    # and DD.MM.YYYY
    date_pattern = r'((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}[\s,]+\d{4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    
    found = re.findall(date_pattern, text, re.I)
    # Clean duplicates
    unique_dates = []
    for d in found:
        if d not in unique_dates:
            unique_dates.append(d)
            
    return [f"Event: {d}" for d in unique_dates[:8]] if unique_dates else ["No specific dates found"]


























