import re

def find_legal_details(text):
    # 1. Check if text actually exists
    if not text or len(text.strip()) < 5:
        return {"Parties": ["PDF UNREADABLE", "CHECK IF SCAN"], "Laws": []}

    # 2. Extract first 10 lines
    lines = [l.strip() for l in text[:2000].split('\n') if len(l.strip()) > 2]
    
    # 3. Look for names in brackets (The most common format)
    found = []
    for line in lines:
        match = re.search(r'\(([^)]+)\)', line)
        if match:
            name = match.group(1).strip().upper()
            if not any(x in name for x in ["APPELLANT", "RESPONDENT", "PETITIONER"]):
                found.append(name)

    # 4. Fallback: If no brackets, take the 3rd and 5th lines (standard layout)
    if len(found) < 2 and len(lines) > 5:
        found.append(lines[2].upper())
        found.append(lines[4].upper())

    return {
        "Parties": [found[0] if len(found) > 0 else "Not detected", 
                    found[1] if len(found) > 1 else "Not detected"],
        "Laws": re.findall(r'(Section\s\d+|Maintenance|CrPC|HMA)', text, re.I)
    }

def extract_timeline(text):
    # This finds any date like February 14, 2023 or 14/02/2023
    date_regex = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}[\s,]+\d{4}|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    found = re.findall(date_regex, text, re.I)
    unique = list(dict.fromkeys([d.strip() for d in found]))
    return [f"Key Date: {d}" for d in unique[:6]] if unique else ["No dates found"]


































