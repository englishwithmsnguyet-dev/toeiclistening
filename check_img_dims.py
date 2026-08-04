import fitz
doc = fitz.open('/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/TÀI LIỆU ETS/ETS 2026/TOEIC ETS 2026- Thay Dinh Van/Final Thay Dinh Van LISTENING ETS 2026 .pdf')

for p in range(21, 24):
    print(f"Page {p+1}:")
    for img in doc[p].get_images():
        print(f"  xref: {img[0]}, width: {img[2]}, height: {img[3]}")
