import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

dang2 = data[2]['theory']

# Group them by logical pairs if they are practice slides
for i, slide in enumerate(dang2):
    print(f"[{i}] Slide {slide.get('slide_index')}: img={len(slide.get('images', []))} text={len(slide.get('text', []))}")
    if slide.get('text') and 'PICTURE' in str(slide['text'][0]):
        print(f"    --> {slide['text'][0][:50]}")
    elif slide.get('text') and 'CẤU TRÚC' in str(slide['text'][0]):
        print(f"    --> CẤU TRÚC CHÍNH slide")
