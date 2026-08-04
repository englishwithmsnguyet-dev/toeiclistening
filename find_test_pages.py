import fitz
import pytesseract
import cv2
import numpy as np

doc = fitz.open('/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/TÀI LIỆU ETS/ETS 2026/TOEIC ETS 2026- Thay Dinh Van/Final Thay Dinh Van LISTENING ETS 2026 .pdf')

for p in [32, 61, 90, 119, 144]:
    if p >= len(doc): continue
    pix = doc[p-1].get_pixmap(dpi=50) # check the page before (1-indexed page 32 is index 31)
    img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY) if pix.n == 3 else img_array
    text = pytesseract.image_to_string(gray)
    print(f"Page {p} (index {p-1}): {text[:50].strip().replace(chr(10), ' ')}")

