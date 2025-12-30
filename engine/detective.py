import re

def find_legal_details(text):
    """
    Extracts Parties and Laws from the text.
    """
    details = {
        "Parties": [],
        "Laws": []
    }
    
    # 1. Simple Regex for Parties (Looking for 'VS' or 'VERSUS')
    party_pattern = r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\s+(?:vs\.?|versus)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)"
    party_match = re.search(party_pattern, text)
    if party_match:
        details["Parties"] = [party_match.group(1), party_match.group(2)]

    # 2. Simple Regex for Common Indian Laws
    law_keywords = ["Hindu Marriage Act", "Section 125", "CrPC", "IPC", "Domestic Violence Act", "Maintenance", "Custody"]
    for law in law_keywords:
        if law.lower() in text.lower():
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    """
    Extracts dates and surrounding context.
    """
    # Pattern for dates like 12.05.2023 or 12/05/2023
    date_pattern = r'(\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    matches = re.findall(date_pattern, text)
    
    timeline = []
    seen = set()
    for m in matches:
        if m not in seen:
            timeline.append(f"Date found: {m}")
            seen.add(m)
        if len(timeline) > 5: break
            
    return timeline





