import re

def extract_timeline(text):
    # 1. Improved Date Pattern
    date_pattern = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})|((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s.-]?\d{1,2}(?:st|nd|rd|th)?[\s,.-]?\d{4})|(\d{1,2}(?:st|nd|rd|th)?[\s.-]?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,.-]?\d{4})'
    
    # 2. Find all dates in the text
    matches = re.findall(date_pattern, text, re.IGNORECASE)
    
    timeline = []
    seen_sentences = set() # To avoid duplicate entries

    for match in matches:
        # Clean up the regex tuple into a single string
        date_str = "".join(match).strip()
        
        # 3. Find the sentence containing this date
        # This looks for the text between periods (.) surrounding the date
        sentence_match = re.search(r'([^.!?]*' + re.escape(date_str) + r'[^.!?]*[.!?])', text)
        
        if sentence_match:
            sentence = sentence_match.group(0).strip()
            # Clean up newlines and extra spaces inside the sentence
            clean_sentence = " ".join(sentence.split())
            
            if clean_sentence not in seen_sentences and len(clean_sentence) > 10:
                # 4. Format the output with an emoji
                timeline.append(f"📅 **{date_str}**: {clean_sentence}")
                seen_sentences.add(clean_sentence)
        
        # 5. Limit to 8-10 events to keep the UI clean
        if len(timeline) >= 10:
            break
                
    return timeline



