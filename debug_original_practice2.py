import json

with open('data/part01_data.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

for i, s in enumerate(old_data[2]['theory']):
    texts = s.get('text', [])
    first = texts[0] if texts else ""
    if 'PICTURE' in first or 'PRACTICE' in first or (not texts and s.get('images')):
        print(f"Index {i} (Slide {i+1}): {first[:50]}")
        print("Images:", s.get('images'))
