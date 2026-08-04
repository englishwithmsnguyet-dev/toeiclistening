import json

with open('data/part01_data.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

for i, slide in enumerate(old_data[2]['theory']):
    if slide.get('audio'):
        print(f"Slide {i+1} has audio: {slide['audio']}")
