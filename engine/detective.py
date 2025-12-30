import re


def find_legal_details(text):
    """
    Advanced detection for Parties and Laws.
    """
    details = {
        "Parties": [],
        "Laws": []
    }
    
    # --- 1. ENHANCED PARTY DETECTION (Targeting formal Headers) ---
    head_text = text[:3000] # Focus on the first few pages
    
    # Pattern A: Look for Appellant vs Respondent style (Common in Delhi High Court)
    # This captures: "NAME ... Appellant Versus NAME ... Respondent"
    app_res_pattern = r"(?s)(.+?)\.\.\.\s*Appellant\s+(?:Versus|Vs\.?)\s+(.+?)\.\.\.\s*Respondent"
    match_ar = re.search(app_res_pattern, head_text, re.IGNORECASE)
    
    if match_ar:
        details["Parties"] = [match_ar.group(1).strip().replace('\n', ' '), 
                              match_ar.group(2).strip().replace('\n', ' ')]
    
    # Pattern B: Look for Title style (e.g., "MEENAL vs. RAJESH")
    if not details["Parties"]:
        vs_pattern = r"([A-Z]{2,}(?:\s[A-Z]{2,})*)\s+(?:VERSUS|V/S|VS\.?)\s+([A-Z]{2,}(?:\s[A-Z]{2,})*)"
        match_vs = re.search(vs_pattern, head_text)
        if match_vs:
            details["Parties"] = [match_vs.group(1).strip(), match_vs.group(2).strip()]

    # Pattern C: Fallback for "In the matter of: Name"
    if not details["Parties"]:
        matter_match = re.search(r"Matter of\s*:\s*([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)", head_text)
        if matter_match:
            details["Parties"] = [matter_match.group(1).strip(), "Unknown"]

    # --- 2. LAW DETECTION ---
    law_keywords = [
        "Section 125", "CrPC", "Maintenance", "Custody", 
        "Hindu Marriage Act", "Domestic Violence Act", "IPC"
    ]
    
    for law in law_keywords:
        if re.search(r'\b' + re.escape(law) + r'\b', text, re.IGNORECASE):
            details["Laws"].append(law)
            
    # Clean up names (remove extra dots or 'and others')
    details["Parties"] = [re.sub(r'\.+', '', p).strip() for p in details["Parties"]]
    
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







