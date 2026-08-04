import json
import re

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

dang2 = data[2]['theory']

def extract_text(html_arr):
    return [re.sub(r'<[^>]+>', '', t).replace('`', '').strip() for t in html_arr if t.strip() and t != '`']

for slide in dang2:
    if slide.get('text') and 'PICTURE' in str(slide['text'][0]):
        print(f"--- Slide {slide['slide_index']} ---")
        texts = extract_text(slide['text'])
        for t in texts:
            print(t)
