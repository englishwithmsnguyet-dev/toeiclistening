import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

for slide in data[1]['theory']:
    if 'BÀI TẬP ÁP DỤNG' in str(slide['text']) or 'BÀI TẬP' in str(slide['text']) or 'PRACTICE' in str(slide['text']).upper():
        print(f"Found title slide at slide_index: {slide['slide_index']}")
        print(slide['text'][0][:200])
