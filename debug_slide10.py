import json

with open('data/part01_data.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

for i, slide in enumerate(old_data[2]['theory'][8:12]):
    print(f"--- Index {8+i} (Slide {9+i}) ---")
    for t in slide.get('text', []):
        print(t[:100])
