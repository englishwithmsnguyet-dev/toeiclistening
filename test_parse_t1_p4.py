import re
import json
import pdfplumber

def parse_part4_questions(pdf_path):
    print(f"Parsing {pdf_path}...")
    text_chunks = []
    
    # Try text extraction first
    with pdfplumber.open(pdf_path) as pdf:
        for i in range(10, min(30, len(pdf.pages))):
            text = pdf.pages[i].extract_text()
            if text:
                text_chunks.append(text)
                
    full_text = "\n".join(text_chunks)
    print(f"Extracted {len(full_text)} characters.")
    
    # If text is empty, it's an image PDF. Let's try to find transcripts.
    if len(full_text) < 100:
        print("This appears to be an image-based PDF or has no text. OCR required.")
        return None

    return full_text

# Run it
text = parse_part4_questions("TOEIC TEST 2025_ TEST 1.pdf")
if text:
    print(text[:1000])
