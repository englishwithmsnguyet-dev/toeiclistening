import cv2
import numpy as np

img_path = '/Users/nguyetpham/.gemini/antigravity/brain/915962ce-dd45-403f-9aab-7380a34b0eab/.user_uploaded/media__1785479782680.png'
img = cv2.imread(img_path)
if img is None:
    print("Cannot read image")
    exit(1)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

boxes = []
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    if w > 100 and h > 100: # filter out text and noise
        boxes.append((x, y, w, h))

boxes.sort(key=lambda b: b[0])

if len(boxes) >= 2:
    left_box = boxes[0]
    right_box = boxes[-1]
    
    x, y, w, h = left_box
    left_img = img[y:y+h, x:x+w]
    cv2.imwrite('data/graphics/part01/look_left.png', left_img)
    
    x, y, w, h = right_box
    right_img = img[y:y+h, x:x+w]
    cv2.imwrite('data/graphics/part01/look_right.png', right_img)
    print(f"Cropped left: {left_box}, right: {right_box}")
else:
    print(f"Found {len(boxes)} boxes, expected at least 2")
