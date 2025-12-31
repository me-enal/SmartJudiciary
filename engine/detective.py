import re

def find_legal_details(text):
    details = {"Parties": ["Not detected", "Not detected"], "Laws": []}
    
    # 1. Clean the header to remove extra dots and spaces
    header = text[:3500]
    header = re.sub(r'\.{2,}', ' ', header)
    
    # 2. Split into lines
    lines = [l.strip() for l in header.split('\n') if len(l.strip()) > 3]

    p1, p2 = "Not detected", "Not detected"

    for line in lines:
        # STRATEGY: Find text inside brackets - e.g. (Anjali Sharma)
        # Most Indian judgments put the actual name in brackets next to "Appellant"
        bracket_match = re.search(r'\(([^)]+)\)', line)
        
        # Look for Petitioner/Appellant
        if any(word in line.upper() for word in ["APPELLANT", "PETITIONER", "PLAINTIFF"]):
            if bracket_match:
                p1 = bracket_match.group(1)
            elif p1 == "Not detected":
                # Fallback: Take first 3 words before words like 'alleges' or 'is'
                p1 = re.split(r'\balleges\b|\bis\b|\bwas\b|\bfiled\b', line, flags=re.I)[0]

        # Look for Respondent/Defendant
        if any(word in line.upper() for word in ["RESPONDENT", "DEFENDANT"]):
            if bracket_match:
                p2 = bracket_match.group(1)
            elif p2 == "Not detected":
                # Fallback: Take first 3 words before 'challenged' or 'arguing'
                p2 = re.split(r'\bchallenged\b|\barguing\b|\bdenies\b|\bis\b', line, flags=re.I)[0]

    # 3. FINAL SCRUB: Remove legal titles from the names
    def scrub(name):
        # Remove common legal noise
        name = re.sub(r'\b(THE|APPELLANT|RESPONDENT|PETITIONER|SMT|SHRI|MR|MS|MRS|ARCHITECT|COURT|FINDS)\b', '', name, flags=re.I)
        # Remove numbers and special characters
        name = re.sub(r'[^a-zA-Z\s]', '', name)
        return name.strip().upper()

    details["Parties"] = [scrub(p1), scrub(p2)]

    # 4. LAW DETECTION
    for law in ["Section 125", "Maintenance", "Hindu Marriage Act", "Custody", "CrPC"]:
        if re.search(r'\b' + re.escape(law) + r'\b', text, re.I):
            details["Laws"].append(law)
            
    return detailss



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
























