import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
json_str = content[start_idx:end_idx]

data = json.loads(json_str)
audit = []

import re
def extract_text(html):
    t = re.sub(r'<[^>]+>', ' ', html)
    return ' '.join(t.split())[:60]

for section in data:
    if 'theory' in section:
        for slide in section['theory']:
            idx = slide['slide_index']
            if idx > 111:
                break
                
            texts = slide.get('text', [])
            text_preview = " | ".join([extract_text(t) for t in texts])
            imgs = slide.get('images', [])
            
            # For slides reformatted with HTML images
            if not imgs:
                imgs_in_html = re.findall(r'src="([^"]+)"', " ".join(texts))
                imgs = [i.split('/')[-1] for i in imgs_in_html]
                
            audit.append(f"Slide {idx:03d} | Images: {imgs} | Text: {text_preview}")

with open('audit_part1.md', 'w', encoding='utf-8') as f:
    for line in audit:
        f.write(line + '\n')
