import fitz
import pytesseract
import cv2
import numpy as np

doc = fitz.open('/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/TÀI LIỆU ETS/ETS 2026/TOEIC ETS 2026- Thay Dinh Van/Final Thay Dinh Van LISTENING ETS 2026 .pdf')

for p in range(0, 15):
    pix = doc[p].get_pixmap(dpi=150)
    img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY) if pix.n == 3 else img_array
    text = pytesseract.image_to_string(gray)
    if "PART 1" in text or "TEST 1" in text:
        print(f"Page {p+1}: found PART 1 or TEST 1!")
        print(text[:200])
