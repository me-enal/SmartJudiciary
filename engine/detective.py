import re


def find_legal_details(text):
    if not text or len(text.strip()) < 10:
        return {
            "Parties": ["PDF UNREADABLE", "CHECK IF SCAN"],
            "Laws": []
        }

    lines = [l.strip() for l in text[:4000].split('\n') if len(l.strip()) > 3]
    found = []

    # Detect parties using VS / VERSUS
    vs_pattern = re.compile(
        r'([A-Z][A-Za-z\s.&]+?)\s+(?:VS\.?|V\.?|VERSUS)\s+([A-Z][A-Za-z\s.&]+)',
        re.I
    )

    for line in lines:
        match = vs_pattern.search(line)
        if match:
            found.append(match.group(1).strip().upper())
            found.append(match.group(2).strip().upper())
            break

    # Fallback: names in brackets
    if len(found) < 2:
        for line in lines:
            match = re.search(r'\(([^)]+)\)', line)
            if match:
                name = match.group(1).strip().upper()
                if not any(x in name for x in
                           ["APPELLANT", "RESPONDENT", "PETITIONER", "DEFENDANT"]):
                    if name not in found:
                        found.append(name)

    # Final fallback
    if len(found) < 2:
        noise = ["COURT", "JUDGE", "ORDER", "JUDGMENT", "DATED"]
        for line in lines:
            up = line.upper()
            if not any(n in up for n in noise):
                clean = re.sub(r'[^A-Z\s]', '', up).strip()
                if 2 <= len(clean.split()) <= 4 and clean not in found:
                    found.append(clean)

    law_patterns = r'(Section\s\d+|CrPC|IPC|HMA|DV\sAct|Domestic\sViolence|Maintenance|Custody)'
    laws_found = list(set(re.findall(law_patterns, text, re.I)))

    return {
        "Parties": [
            found[0] if len(found) > 0 else "Not detected",
            found[1] if len(found) > 1 else "Not detected"
        ],
        "Laws": laws_found
    }


def extract_timeline(text):
    date_regex = (
        r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
        r'[a-z]*\s+\d{1,2}[\s,]+\d{4}'
        r'|\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})'
    )

    found = re.findall(date_regex, text, re.I)
    unique = list(dict.fromkeys([d.strip() for d in found]))

    if not unique:
        return ["No dates found"]

    return [f"Key Date: {d}" for d in unique[:6]]

    





































