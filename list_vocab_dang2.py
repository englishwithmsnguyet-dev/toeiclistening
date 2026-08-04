import json
import re

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
json_str = content[start_idx:end_idx]
data = json.loads(json_str)

def strip_tags(text):
    return re.sub(r'<[^>]+>', ' ', text).strip()

for section in data:
    if 'theory' in section:
        for slide in section['theory']:
            idx = slide['slide_index']
            if 118 <= idx <= 133:
                texts = [strip_tags(t) for t in slide.get('text', [])]
                if 'CÁC ĐỘNG TỪ THƯỜNG GẶP' in texts[0]:
                    print(f"Slide {idx}: {' | '.join(texts[1:])}")
