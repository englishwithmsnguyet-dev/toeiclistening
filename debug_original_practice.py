import json

with open('data/part01_data.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

for i, s in enumerate(old_data[2]['theory']):
    first = s.get('text', [''])[0]
    if 'PICTURE' in first or 'PRACTICE' in first:
        print(f"Index {i} (Slide {i+1}): {first[:50]}")
        print("Images:", s.get('images'))
