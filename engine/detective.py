import re

def find_legal_details(text):
    details = {"Parties": ["Not detected", "Not detected"], "Laws": []}
    
    # 1. Focus on the header (First 3000 chars)
    header = text[:3000]
    lines = [l.strip() for l in header.split('\n') if len(l.strip()) > 2]

    p1, p2 = "Not detected", "Not detected"

    for line in lines:
        # STRATEGY: Look for names inside brackets (Anjali Sharma)
        # This is the most accurate way when the text is messy
        name_in_brackets = re.findall(r'\(([^)]+)\)', line)
        
        if "APPELLANT" in line.upper() or "PETITIONER" in line.upper():
            if name_in_brackets:
                # Take the first bracket content that isn't just a number
                for cand in name_in_brackets:
                    if not cand.isdigit():
                        p1 = cand
                        break
            else:
                # Fallback: Take text before "alleges" or "is"
                p1 = re.split(r'\balleges\b|\bis\b|\bwas\b|\bhas\b', line, flags=re.I)[0]

        if "RESPONDENT" in line.upper() or "DEFENDANT" in line.upper():
            if name_in_brackets:
                for cand in name_in_brackets:
                    if not cand.isdigit():
                        p2 = cand
                        break
            else:
                # Fallback: Take text before "challenged" or "arguing"
                p2 = re.split(r'\bchallenged\b|\barguing\b|\bis\b|\bfiled\b', line, flags=re.I)[0]

    # 2. FINAL CLEANUP: Strip titles and legal jargon
    def clean_name(name):
        # Remove "The", "Appellant", "Respondent" and symbols
        name = re.sub(r'\b(THE|APPELLANT|RESPONDENT|PETITIONER|DEFENDANT|SMT|SHRI|MR|MS|MRS)\b', '', name, flags=re.I)
        name = re.sub(r'[^a-zA-Z\s]', '', name)
        return name.strip().upper()

    details["Parties"] = [clean_name(p1) or "Not detected", clean_name(p2) or "Not detected"]

    # 3. LAW DETECTION
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























