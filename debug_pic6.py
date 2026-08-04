import json
import re

with open('data/part01_data.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

for slide in old_data[2]['theory']:
    if slide.get('text') and isinstance(slide['text'], list) and len(slide['text']) > 0:
        if 'PICTURE 06' in slide['text'][0]:
            print(slide['text'])
