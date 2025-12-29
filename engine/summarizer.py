from transformers import pipeline

# Load the summarization 'brain'
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def make_summary(text):
    # Condense the text (limit input to 1024 characters for speed)
    result = summarizer(text[:1024], max_length=150, min_length=50, do_sample=False)
    return result[0]['summary_text']