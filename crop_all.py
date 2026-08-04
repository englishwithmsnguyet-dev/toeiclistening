import fitz
import cv2
import numpy as np

doc = fitz.open('/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/TÀI LIỆU ETS/ETS 2026/TOEIC ETS 2026- Thay Dinh Van/Final Thay Dinh Van LISTENING ETS 2026 .pdf')

output_dir = "/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/BÀI GIẢNG/toeic_listening_web/data/graphics/part01"

def crop_test(t_idx):
    start_page = 3 + (t_idx - 1) * 29
    
    # Page 1: Q1 (bottom)
    pix = doc[start_page].get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 3: img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(f"{output_dir}/ets26_t0{t_idx}_q01.jpg", img[900:1500, 100:1100])
    
    # Page 2: Q2 (top), Q3 (bottom)
    pix = doc[start_page + 1].get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 3: img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(f"{output_dir}/ets26_t0{t_idx}_q02.jpg", img[200:800, 100:1100])
    cv2.imwrite(f"{output_dir}/ets26_t0{t_idx}_q03.jpg", img[900:1500, 100:1100])

    # Page 3: Q4 (top), Q5 (bottom)
    pix = doc[start_page + 2].get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 3: img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(f"{output_dir}/ets26_t0{t_idx}_q04.jpg", img[200:800, 100:1100])
    cv2.imwrite(f"{output_dir}/ets26_t0{t_idx}_q05.jpg", img[900:1500, 100:1100])

    # Page 4: Q6 (top)
    pix = doc[start_page + 3].get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 3: img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(f"{output_dir}/ets26_t0{t_idx}_q06.jpg", img[200:800, 100:1100])

for i in range(1, 6):
    crop_test(i)
