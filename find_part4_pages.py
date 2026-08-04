import fitz
import pytesseract
from PIL import Image
import os

pdf_path = '../TOEIC PART 04/ETS 2026/Final Thay Dinh Van LISTENING ETS 2026 .pdf'
doc = fitz.open(pdf_path)

print('Finding PART 4 pages...')
pages_with_part4 = []

# Scan every 5th page to quickly locate the start of tests
for i in range(0, doc.page_count, 2):
    page = doc[i]
    pix = page.get_pixmap(dpi=75) # lower dpi for faster scan
    img_path = f'fast_{i}.png'
    pix.save(img_path)
    text = pytesseract.image_to_string(Image.open(img_path))
    if 'PART 4' in text or '71' in text or 'directions' in text.lower():
        pages_with_part4.append(i)
        print(f'Found keywords on page {i}')
    os.remove(img_path)

print('Pages with keywords:', pages_with_part4)
