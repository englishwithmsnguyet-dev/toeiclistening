import json

with open('data/part01_data.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

for i, s in enumerate(old_data[2]['theory']):
    texts = s.get('text', [])
    if texts:
        first = texts[0]
        if 'CẤU TRÚC' in first.upper():
            print(f"Found at index {i}:")
            print("Images:", s.get('images'))
            for t in texts:
                print(t)
