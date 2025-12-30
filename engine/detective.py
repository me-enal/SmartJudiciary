import re

def find_legal_details(text):
    details = {"Parties": [], "Laws": []}
    header = text[:4000]

    # Cleaned regex for Parties
    # This captures Name ... Petitioner vs Name ... Respondent
    try:
        formal_pattern = r"(?s)(.*?)\s*\.\.\.\s*(?:Appellant|Petitioner|Applicant).*?(?:VERSUS|VS\.?|V/S).*?(.*?)\s*\.\.\.\s*Respondent"
        match = re.search(formal_pattern, header, re.IGNORECASE)

        if match:
            p1 = re.sub(r'[\.\d\n\r]+', ' ', match.group(1)).strip()
            p2 = re.sub(r'[\.\d\n\r]+', ' ', match.group(2)).strip()
            details["Parties"] = [p1[:50], p2[:50]]
        else:
            # Simple fallback
            details["Parties"] = ["Not detected", "Not detected"]
    except:
        details["Parties"] = ["Error in parsing", "Error in parsing"]

    # Law detection
    laws = ["Section 125", "CrPC", "Maintenance", "Custody", "Hindu Marriage Act"]
    for law in laws:
        if law.lower() in text.lower():
            details["Laws"].append(law)
            
    return details

def extract_timeline(text):
    # Very simple date finder to avoid memory crashes
    date_regex = r'(\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    matches = re.findall(date_regex, text)
    unique_dates = list(set(matches))
    return [f"Key Date: {d}" for d in unique_dates[:5]]







