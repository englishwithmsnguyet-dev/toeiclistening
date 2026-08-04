import json

with open('data/part01_data.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

for i, s in enumerate(old_data[2]['theory'][:3]):
    print(f"--- Slide {i} ---")
    for t in s.get('text', []):
        print(t)
