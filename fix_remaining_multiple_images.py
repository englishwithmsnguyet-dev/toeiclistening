import json
import re

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
json_str = content[start_idx:end_idx]
data = json.loads(json_str)

def strip_tags(text):
    return re.sub(r'<[^>]+>', '', text).strip()

count = 0

for section in data:
    if 'theory' in section:
        for slide in section['theory']:
            # Only target slides that still have exactly 2 images in the array
            # (The ones I already fixed have 0 images in the array)
            if len(slide.get('images', [])) == 2:
                texts = slide.get('text', [])
                
                # Check if it's an example slide (not a title/vocab slide)
                # Example slides usually start with English phrase colored green #00B050
                if len(texts) >= 4 and '#00B050' in texts[0] and '#FF0000' not in texts[0]:
                    
                    left_eng = ""
                    right_eng = ""
                    left_vie = ""
                    right_vie = ""
                    
                    if len(texts) == 4:
                        left_eng = strip_tags(texts[0])
                        right_eng = strip_tags(texts[1])
                        left_vie = strip_tags(texts[2])
                        right_vie = strip_tags(texts[3])
                    elif len(texts) == 6:
                        left_eng = strip_tags(texts[0])
                        right_eng = strip_tags(texts[1])
                        left_vie = strip_tags(texts[2]) + " " + strip_tags(texts[3])
                        right_vie = strip_tags(texts[4]) + " " + strip_tags(texts[5])
                    else:
                        continue # Skip weird formats just in case
                        
                    img1 = slide['images'][0]
                    img2 = slide['images'][1]
                    
                    html = f'''<div style="display: flex; flex-direction: row; gap: 32px; justify-content: center; width: 100%; align-items: flex-start; margin-top: 10px;">
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/{img1}" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">{left_eng}</strong></div><div style="margin-bottom: 8px;">{left_vie}</div>
    </div>
  </div>
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/{img2}" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">{right_eng}</strong></div><div style="margin-bottom: 8px;">{right_vie}</div>
    </div>
  </div>
</div>'''
                    
                    slide['text'] = [html]
                    slide['images'] = []
                    count += 1

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")

print(f"Successfully fixed {count} remaining multiple-image slides.")
