from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

import streamlit as st

@st.cache_resource
def load_summarizer():
    model_name = "sshleifer/distilbart-cnn-12-6"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

def make_summary(text):
    if not text or len(text.strip()) < 100:
        return "Text too short for a meaningful summary."

    try:
        tokenizer, model = load_summarizer()

        inputs = tokenizer(
            text[:3000], 
            return_tensors="pt", 
            max_length=1024, 
            truncation=True
        )

   
        summary_ids = model.generate(
            inputs["input_ids"], 
            max_length=150, 
            min_length=40, 
            length_penalty=2.0, 
            num_beams=4, 
            early_stopping=True
        )

        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary

    except Exception as e:
        return f"Summarization failed: {str(e)}"

