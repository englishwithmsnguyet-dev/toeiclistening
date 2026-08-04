import json

with open('data/part01_data.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

for i, section in enumerate(old_data):
    if 'theory' in section:
        for j, s in enumerate(section['theory']):
            for t in s.get('text', []):
                if 'CẤU TRÚC' in t.upper():
                    print(f"Section {i} (Dạng {i}), Slide {j}: {t}")
