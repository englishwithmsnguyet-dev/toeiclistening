import fitz
import pytesseract
from PIL import Image
import os
import json
import re

pdf_path = '../TOEIC PART 04/ETS 2026/Final Thay Dinh Van LISTENING ETS 2026 .pdf'
doc = fitz.open(pdf_path)

print("Starting OCR extraction for pages 10 to 80...")
full_text = ""
for i in range(10, 80):
    page = doc[i]
    pix = page.get_pixmap(dpi=150)
    img_path = f'tmp_page_{i}.png'
    pix.save(img_path)
    
    text = pytesseract.image_to_string(Image.open(img_path))
    full_text += f"\n--- PAGE {i} ---\n" + text
    
    os.remove(img_path)

with open("raw_ocr_p4.txt", "w", encoding="utf-8") as f:
    f.write(full_text)
print("Finished OCR! Saved to raw_ocr_p4.txt")
