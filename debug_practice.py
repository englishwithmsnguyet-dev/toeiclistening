import json
import re

with open('data/part01_data.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

dang2_raw = old_data[2]['theory']

def clean_text(t):
    return re.sub(r'<[^>]+>', '', t).replace('`', '').strip()

def get_first_text(slide):
    if slide.get('text') and isinstance(slide['text'], list) and len(slide['text']) > 0:
        return slide['text'][0]
    return ""

count = 0
for i in range(len(dang2_raw)):
    slide = dang2_raw[i]
    first_text = get_first_text(slide)
    
    if 'PICTURE' in first_text and len(slide.get('images', [])) == 1:
        print(f"Matched single: {first_text}")
        count += 1
        
    if len(slide.get('images', [])) == 1 and len(slide.get('text', [])) == 0:
        if i + 1 < len(dang2_raw) and 'PICTURE' in get_first_text(dang2_raw[i+1]):
            print(f"Matched split: img={slide['images']} + text={get_first_text(dang2_raw[i+1])}")
            count += 1
            
print(f"Total matched practice: {count}")
