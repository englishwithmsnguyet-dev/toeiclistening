import json
import re

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
json_str = content[start_idx:end_idx]

data = json.loads(json_str)

for section in data:
    if 'theory' in section:
        for slide in section['theory']:
            idx = slide['slide_index']
            if idx > 111: break
            
            texts = slide.get('text', [])
            if not texts: continue
            
            html = texts[0]
            if 'display: flex' in html: # it's a multiple image slide
                imgs = re.findall(r'src="([^"]+)"', html)
                imgs = [i.split('/')[-1] for i in imgs]
                
                # Extract english text
                eng_texts = re.findall(r'<strong style="color: #00B050;">([^<]+)</strong>', html)
                if not eng_texts:
                    # check if wearing
                    if 'wearing a long-sleeved shirt' in html:
                        eng_texts = ['wearing a long-sleeved shirt', 'wearing sunglasses']
                
                print(f"Slide {idx:02d}: {imgs} | {eng_texts}")
