import json

with open('data/part01_data.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

for slide in old_data[2]['theory'][:10]:
    for t in slide.get('text', []):
        if '#0070C0' in t:
            print(t)
