import fitz
import cv2
import numpy as np

doc = fitz.open('/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/TÀI LIỆU ETS/ETS 2026/TOEIC ETS 2026- Thay Dinh Van/Final Thay Dinh Van LISTENING ETS 2026 .pdf')

pix = doc[6].get_pixmap(dpi=150)
img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
if pix.n == 3: img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

cv2.imwrite(f"/Users/nguyetpham/.gemini/antigravity/brain/915962ce-dd45-403f-9aab-7380a34b0eab/scratch/t1_q6.png", img[200:800, 100:1100])
