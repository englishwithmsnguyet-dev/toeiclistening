import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

for slide in data[2]['theory']:
    idx = slide.get('slide_index')
    if idx in [9, 11, 17]:
        print(f"\n======== SLIDE {idx} ========")
        print(slide['text'][0])
