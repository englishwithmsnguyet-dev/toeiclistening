import pdfplumber
import json
import re
import os

pdf_path = "TOEIC TEST 2025_ TEST 1.pdf"

if not os.path.exists(pdf_path):
    print(f"Error: {pdf_path} not found.")
    exit(1)

text_chunks = []
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            text_chunks.append(text)

full_text = "\n".join(text_chunks)
print(f"Extracted {len(full_text)} characters.")

# Look for Part 4
idx = full_text.find("PART 4")
if idx == -1:
    idx = full_text.find("Part 4")
    
if idx != -1:
    print(f"Found Part 4 at index {idx}")
    print(full_text[idx:idx+1000])
else:
    print("Part 4 not found!")

