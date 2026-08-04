import fitz
import cv2
import numpy as np

doc = fitz.open('/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/TÀI LIỆU ETS/ETS 2026/TOEIC ETS 2026- Thay Dinh Van/Final Thay Dinh Van LISTENING ETS 2026 .pdf')

output_dir = "/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/BÀI GIẢNG/toeic_listening_web/data/graphics/part01"

def crop_test(t_idx):
    start_page = 3 + (t_idx - 1) * 29
    
    # Page 1: Example (skip), Q1
    pix = doc[start_page].get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 3: img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(f"{output_dir}/ets26_t0{t_idx}_q01.jpg", img[900:1500, 100:1100])
    
    # Page 2: Q2, Q3
    pix = doc[start_page + 1].get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 3: img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(f"{output_dir}/ets26_t0{t_idx}_q02.jpg", img[200:800, 100:1100])
    cv2.imwrite(f"{output_dir}/ets26_t0{t_idx}_q03.jpg", img[900:1500, 100:1100])

    # Page 3: Q4, Q5, wait Q6 is on page 3?
    # Actually Q4 and Q5 are on Page 3 (start_page+2)
    # Wait, earlier: 
    # crop_page(32, "0", "1", "t2") -> 0 is top, 1 is bottom. Q1 is bottom of page 1.
    # crop_page(33, "2", "3", "t2") -> Q2 is top, Q3 is bottom of page 2.
    # crop_page(34, "4", "5", "t2") -> Q4 is top, Q5 is bottom of page 3.
    # Wait, where is Q6? Q6 is usually on the NEXT page!
    
