import fitz
import cv2
import numpy as np

doc = fitz.open('/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/TÀI LIỆU ETS/ETS 2026/TOEIC ETS 2026- Thay Dinh Van/Final Thay Dinh Van LISTENING ETS 2026 .pdf')

# Page 5 (Index 4) contains Q3 and Q4
pix = doc[4].get_pixmap(dpi=150)
img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
if pix.n == 3: img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

# Dimensions at 150 dpi: approx 1237 x 1754
h, w, _ = img.shape
print(f"Image size: {w}x{h}")

# Q3 is usually on the top half, Q4 on the bottom half
# Let's crop top half and bottom half and check
q3_crop = img[200:800, 100:1100]
q4_crop = img[900:1500, 100:1100]

cv2.imwrite("/Users/nguyetpham/.gemini/antigravity/brain/915962ce-dd45-403f-9aab-7380a34b0eab/q3_crop.png", q3_crop)
cv2.imwrite("/Users/nguyetpham/.gemini/antigravity/brain/915962ce-dd45-403f-9aab-7380a34b0eab/q4_crop.png", q4_crop)
