import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

dang2 = data[2]['theory']

for i, slide in enumerate(dang2):
    print(f"[{i}] Slide_Index: {slide.get('slide_index')} | Images: {len(slide.get('images', []))} | Text count: {len(slide.get('text', []))}")
    if slide.get('text'):
        print(f"   First text: {slide['text'][0][:150]}")
