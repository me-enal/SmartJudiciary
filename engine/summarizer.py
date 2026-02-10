from transformers import pipeline
import streamlit as st

def make_summary(text):
    if not text or len(text) < 100:
        return "Text too short to summarize."

    try:
      
        summarizer = pipeline(
            "summarization", 
            model="sshleifer/distilbart-cnn-12-6",
            framework="pt" 
        )
        
        input_text = text[:1024] 
        
        summary = summarizer(input_text, max_length=150, min_length=50, do_sample=False)
        return summary[0]['summary_text']
        
    except Exception as e:
        return f"Summary Error: {str(e)}"
