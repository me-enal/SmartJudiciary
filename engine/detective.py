import re

def find_legal_details(text):
    """
    Extracts Parties and Laws using a robust multi-pattern approach.
    """
    details = {
        "Parties": [],
        "Laws": []
    }
    
    # --- 1. ENHANCED PARTY DETECTION ---
    # We look for the "VS" block which usually appears in the first 2000 chars
    head_text = text[:2000] 
    
    # Pattern A: Standard [Name] VS [Name] (Handles multiple lines and ALL CAPS)
    # The (?s) flag allows the dot . to match newlines
    vs_pattern = r"(?i)(.+?)\s+(?:VERSUS|V/S|VS\.?)\s+(.+?)(?=\n\n|\s{2,}|Petitioner|Respondent|JUDGMENT|$)"
    vs_match = re.search(vs_pattern, head_text, re.DOTALL)
    
    if vs_match:
        p1 = vs_match.group(1).strip().split('\n')[-1] # Take the line closest to 'VS'
        p2 = vs_match.group(2).strip().split('\n')[0]  # Take the line immediately after 'VS'
        details["Parties"] = [p1.strip(), p2.strip()]
    
    # Pattern B: If Pattern A fails, look for 'Petitioner' and 'Respondent' labels
    if not details["Parties"]:
        pet_match = re.search(r"(?i)(.+?)\s*\.{3,}\s*Petitioner", head_text)
        res_match = re.search(r"(?i)(.+?)\s*\.{3,}\s*Respondent", head_text)
        if pet_match and res_match:
            details["Parties"] = [pet_match.group(1).strip(), res_match.group(1).strip()]

    # --- 2. ENHANCED LAW DETECTION ---
    # Expanded list for better coverage in Indian Family Law
    law_keywords = [
        "Hindu Marriage Act", "Section 125", "CrPC", "IPC", 
        "Domestic Violence Act", "Maintenance", "Custody", 
        "Special Marriage Act", "Hindu Succession Act",
        "Family Courts Act", "Indian Evidence Act"
    ]
    
    # Use word boundaries (\b) to avoid partial matches
    for law in law_keywords:
        if re.search(r'\b' + re.escape(law) + r'\b', text, re.IGNORECASE):
            details["Laws"].append(law)
            
    # Clean up results (remove duplicates)
    details["Laws"] = list(set(details["Laws"]))
    
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






