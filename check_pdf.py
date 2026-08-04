import fitz
PDF_PATH = '/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/TÀI LIỆU ETS/ETS 2026/TOEIC ETS 2026- Thay Dinh Van/Final Thay Dinh Van LISTENING ETS 2026 .pdf'
doc = fitz.open(PDF_PATH)
for p in range(15, 25):
    text = doc[p].get_text()
    if "PART 1" in text or "TEST" in text:
        print(f"Page {p+1}: {text[:100].replace(chr(10), ' ')}")
