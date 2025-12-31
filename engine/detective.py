import re

def find_legal_details(text):
    details = {"Parties": ["Not detected", "Not detected"], "Laws": []}
    header = text[:3000]
    lines = [l.strip() for l in header.split('\n') if len(l.strip()) > 2]

    p1, p2 = "Not detected", "Not detected"

    for line in lines:
        # 1. FIND NAME IN BRACKETS (e.g., "the appellant (Anjali Sharma)")
        bracket_match = re.search(r'\(([^)]+)\)', line)
        
        if "APPELLANT" in line.upper() or "PETITIONER" in line.upper():
            if bracket_match:
                p1 = bracket_match.group(1)
            else:
                # If no brackets, take words before "alleges" or "was"
                p1 = re.split(r'\balleges\b|\bwas\b|\bis\b|\bfiled\b', line, flags=re.I)[0]
                p1 = re.sub(r'\b(the|appellant|petitioner)\b', '', p1, flags=re.I).strip()

        if "RESPONDENT" in line.upper() or "DEFENDANT" in line.upper():
            if "challenged" in line.lower() or "arguing" in line.lower():
                # Take words before "challenged"
                p2 = re.split(r'\bchallenged\b|\barguing\b|\bis\b|\bdenies\b', line, flags=re.I)[0]
                p2 = re.sub(r'\b(the|respondent|defendant)\b', '', p2, flags=re.I).strip()

    # Final Clean: Remove numbers/years from names
    def clean_name(name):
        name = re.sub(r'[^a-zA-Z\s]', '', name)
        return name.strip().upper()

    details["Parties"] = [clean_name(p1), clean_name(p2)]

    # 2. LAW DETECTION
    for law in ["Section 125", "Maintenance", "Hindu Marriage Act", "Custody", "CrPC"]:
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






















