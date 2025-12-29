import spacy
import re

# Load the high-accuracy transformer model
# Change "en_core_web_trf" to "en_core_web_sm"
nlp = spacy.load("en_core_web_sm")

def find_legal_details(text):
    """Extracts Names and Laws from the judgment text."""
    # We analyze the first 5000 characters for names and laws
    doc = nlp(text[:5000])
    
    parties = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    laws = [ent.text for ent in doc.ents if ent.label_ in ["LAW", "GPE", "ORG"]]
    
    return {
        "Parties": list(set(parties)), 
        "Laws": list(set(laws))
    }

def extract_timeline(text):
    """Finds dates and events to create a chronology for the lawyer."""
    # This pattern looks for dates like 21.03.2022, 15/08/1947, or 10 January 2021
    date_pattern = r'(\d{1,2}[-/.\s]*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[-/.\s,]*\d{2,4}|\d{1,2}/\d{1,2}/\d{2,4})'
    
    # Split text into sentences to find context for the dates
    sentences = text.split('.')
    timeline = []
    
    for sent in sentences:
        found_date = re.search(date_pattern, sent)
        if found_date:
            # Clean up the sentence and add to list
            event = sent.strip()
            if len(event) > 10:  # Ignore tiny fragments
                timeline.append(f"📅 **{found_date.group()}**: {event[:100]}...")
        
        # Limit to the first 8 important dates to keep the UI clean
        if len(timeline) >= 8:
            break
            

    return timeline
