import fitz
doc = fitz.open('/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/TÀI LIỆU ETS/ETS 2026/TOEIC ETS 2026- Thay Dinh Van/Final Thay Dinh Van LISTENING ETS 2026 .pdf')

# Let's render page 21 (index 20) and 22 (index 21)
pix1 = doc[21].get_pixmap(dpi=150)
pix1.save("/Users/nguyetpham/.gemini/antigravity/brain/915962ce-dd45-403f-9aab-7380a34b0eab/page_22.png")

pix2 = doc[22].get_pixmap(dpi=150)
pix2.save("/Users/nguyetpham/.gemini/antigravity/brain/915962ce-dd45-403f-9aab-7380a34b0eab/page_23.png")

pix3 = doc[23].get_pixmap(dpi=150)
pix3.save("/Users/nguyetpham/.gemini/antigravity/brain/915962ce-dd45-403f-9aab-7380a34b0eab/page_24.png")
