import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
json_str = content[start_idx:end_idx]

data = json.loads(json_str)

for section in data:
    if 'theory' in section:
        for slide in section['theory']:
            idx = slide['slide_index']
            if idx > 111:
                texts = slide.get('text', [])
                text_str = " ".join(texts).lower()
                if 'monitor' in text_str or 'map' in text_str or 'look' in text_str:
                    print(f"Slide {idx}: {texts}")
