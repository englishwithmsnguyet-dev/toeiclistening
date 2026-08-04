import pytesseract
import cv2
import glob
import re

for i in range(1, 10):
    fname = f"data/graphics/part01/ets26_t01_q0{i}.jpg"
    img = cv2.imread(fname)
    if img is None: continue
    # The question number is usually on the left or top left
    text = pytesseract.image_to_string(img)
    # Search for "1.", "2.", "3." etc.
    print(f"--- {fname} ---")
    lines = text.split('\n')
    for line in lines:
        if line.strip():
            print(line.strip()[:100])
