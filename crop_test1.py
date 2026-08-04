import fitz
import cv2
import numpy as np

doc = fitz.open('/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/TÀI LIỆU ETS/ETS 2026/TOEIC ETS 2026- Thay Dinh Van/Final Thay Dinh Van LISTENING ETS 2026 .pdf')

# T1: pages 3, 4, 5 (0-indexed)
def crop_page(p_idx, q1, q2, p_name):
    pix = doc[p_idx].get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 3: img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # Q1
    cv2.imwrite(f"/Users/nguyetpham/.gemini/antigravity/brain/915962ce-dd45-403f-9aab-7380a34b0eab/scratch/t1_q{q1}.png", img[200:800, 100:1100])
    # Q2
    cv2.imwrite(f"/Users/nguyetpham/.gemini/antigravity/brain/915962ce-dd45-403f-9aab-7380a34b0eab/scratch/t1_q{q2}.png", img[900:1500, 100:1100])

crop_page(3, "0", "1", "pg4") # Example is 0, Q1 is 1
crop_page(4, "2", "3", "pg5")
crop_page(5, "4", "5", "pg6")
