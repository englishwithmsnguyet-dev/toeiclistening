import fitz
import cv2
import numpy as np
import os

PDF_PATH = '/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/TÀI LIỆU ETS/ETS 2026/TOEIC ETS 2026- Thay Dinh Van/Final Thay Dinh Van LISTENING ETS 2026 .pdf'
GRAPHICS_DIR = 'data/graphics/part01'

doc = fitz.open(PDF_PATH)

def extract_photos_from_page(page_idx):
    # Render page at 150 DPI
    pix = doc[page_idx].get_pixmap(dpi=150)
    img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    
    if pix.n == 4:
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
    elif pix.n == 3:
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    else:
        img_cv = img_array

    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    # Adaptive threshold to find dark borders/photos
    # Photos are usually grayscale or color, but they have a lot of edges.
    # A simple way to find photos is to find large rectangular contours.
    
    # Apply blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Edge detection
    edges = cv2.Canny(blurred, 50, 150)
    
    # Dilate to connect edges
    kernel = np.ones((5,5), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=2)
    
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    photos = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        # Page size is approx 1200 x 1700 at 150 dpi
        # Photos are usually 400x300 to 800x600
        if area > 80000 and area < 800000 and w > 200 and h > 200:
            # Check if it's somewhat rectangular
            if 0.5 < (w/h) < 2.0:
                # To avoid text blocks, we can just save the crop and check.
                # Usually text blocks don't form a perfect large solid rectangle in Canny unless boxed.
                # Actually, ETS photos are boxed. 
                photos.append((x, y, w, h))
                
    # Filter overlapping boxes
    final_photos = []
    for p in photos:
        overlap = False
        for fp in final_photos:
            # If centers are close, it's the same
            cx1, cy1 = p[0] + p[2]/2, p[1] + p[3]/2
            cx2, cy2 = fp[0] + fp[2]/2, fp[1] + fp[3]/2
            if abs(cx1 - cx2) < 50 and abs(cy1 - cy2) < 50:
                overlap = True
                break
        if not overlap:
            final_photos.append(p)
            
    # Sort by Y then X
    final_photos.sort(key=lambda b: (b[1] // 100, b[0]))
    
    cropped_imgs = []
    for (x, y, w, h) in final_photos:
        # Add a slight padding if possible
        pad = 5
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(img_cv.shape[1], x + w + pad)
        y2 = min(img_cv.shape[0], y + h + pad)
        
        crop = img_cv[y1:y2, x1:x2]
        cropped_imgs.append((x, y, crop))
        
    return cropped_imgs

# Test on page 21 (Index 20)
crops = extract_photos_from_page(21)
print(f"Found {len(crops)} photos on page 22")
for idx, (x, y, crop) in enumerate(crops):
    cv2.imwrite(f"/Users/nguyetpham/.gemini/antigravity/brain/915962ce-dd45-403f-9aab-7380a34b0eab/crop_test_{idx}.png", crop)
