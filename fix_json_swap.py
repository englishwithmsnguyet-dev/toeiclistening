import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

targets = [
    'pushing the luggage', 
    'pulling a cart', 
    'reaching into a bag', 
    'wearing a long-sleeved shirt', 
    'putting on gloves', 
    'working in an office', 
    'writing on a notebook', 
    'folding a towel', 
    'wiping a window'
]

import re

for section in data:
    if 'theory' in section:
        for slide in section['theory']:
            if not slide.get('text'): continue
            html = slide['text'][0]
            
            for target in targets:
                if target in html:
                    # Found the target, let's swap the image srcs!
                    imgs = re.findall(r'src="([^"]+)"', html)
                    if len(imgs) == 2:
                        new_html = html.replace(imgs[0], 'TEMP_IMG')
                        new_html = new_html.replace(imgs[1], imgs[0])
                        new_html = new_html.replace('TEMP_IMG', imgs[1])
                        slide['text'][0] = new_html
                        print(f"Swapped images for {target}")
                        break

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")

print("Done JSON swap.")
