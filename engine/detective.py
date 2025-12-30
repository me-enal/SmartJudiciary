import re

def extract_timeline(text):
    # 1. This pattern is much broader to catch PDF-style dates
    # Matches: 12.05.2023, 12/05/23, May 12 2023, 12th August 2022, etc.
    date_pattern = r'(\d{1,4}[.\-/]\d{1,2}[.\-/]\d{2,4})|((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s.,]*\d{1,2}(?:st|nd|rd|th)?[\s.,]+\d{4})|(\d{1,2}(?:st|nd|rd|th)?[\s.,]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s.,]+\d{4})'
    
    # Pre-process text to remove multiple spaces/newlines which break regex
    clean_text = " ".join(text.split())
    
    # 2. Find all matches
    matches = re.findall(date_pattern, clean_text, re.IGNORECASE)
    
    timeline = []
    seen_dates = set()

    for match in matches:
        # Reconstruct the date string from the regex groups
        date_str = "".join(match).strip()
        if not date_str or date_str in seen_dates:
            continue
            
        # 3. Grab the surrounding sentence (approx 150 characters)
        # We look for the date and take 60 chars before and 90 chars after
        start_idx = clean_text.find(date_str)
        if start_idx != -1:
            start = max(0, start_idx - 60)
            end = min(len(clean_text), start_idx + 120)
            context = clean_text[start:end].strip()
            
            # Add ellipses if we are cutting off text
            formatted_context = f"...{context}..."
            
            timeline.append(f"📅 **{date_str}**: {formatted_context}")
            seen_dates.add(date_str)
        
        if len(timeline) >= 10:
            break
                
    return timeline



