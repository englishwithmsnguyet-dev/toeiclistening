import json
import re

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

dang2 = data[2]['theory']
new_theory = []

def clean_text(t):
    return re.sub(r'<[^>]+>', '', t).replace('`', '').strip()

# We will iterate through original dang2 and process them
i = 0
while i < len(dang2):
    slide = dang2[i]
    
    # 1. Skip CẤU TRÚC CHÍNH slides (Slide 37, 38, Slide 4)
    if slide.get('text') and len(slide['text']) > 0:
        if 'CẤU TRÚC' in slide['text'][0] or 'CẤU TRÚC' in clean_text(slide['text'][0]).upper():
            i += 1
            continue
    
    # 2. Handle Title slide
    if slide.get('slide_index') == 1:
        new_theory.append(slide)
        i += 1
        continue
    
    # 3. Handle Theory Slides (usually index 2 to 23)
    # We will just dump them as nicely formatted HTML.
    # Wait, if they have exactly 2 images and 5 texts, we know the pattern.
    if len(slide.get('images', [])) == 2 and len(slide.get('text', [])) >= 5:
        texts = slide['text']
        imgs = slide['images']
        title = texts[0]
        html = f"""<div style="text-align: center; margin-bottom: 24px; font-size: 1.5rem;">{title}</div>
<div style="display: flex; flex-direction: row; gap: 32px; justify-content: center; width: 100%; align-items: flex-start;">
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center;">
    <img src="data/graphics/part01/{imgs[0]}" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;">{texts[1]}</div>
      <div style="margin-bottom: 8px; color: var(--text-muted);">{texts[3]}</div>
    </div>
  </div>
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center;">
    <img src="data/graphics/part01/{imgs[1]}" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;">{texts[2]}</div>
      <div style="margin-bottom: 8px; color: var(--text-muted);">{texts[4]}</div>
    </div>
  </div>
</div>"""
        slide['text'] = [html]
        new_theory.append(slide)
        i += 1
        continue
    
    # 4. Handle other theory slides (1 image, multi-lines of text)
    if 'PICTURE' not in slide.get('text', [''])[0] and 'PRACTICE' not in slide.get('text', [''])[0]:
        # Just wrap the text in a nice div
        if len(slide.get('images', [])) == 1 and len(slide.get('text', [])) > 0:
            html = f"""<div style="display: flex; flex-direction: row; gap: 32px; align-items: center; justify-content: center; width: 100%;">
  <div style="flex: 1; max-width: 50%;">
    <img src="data/graphics/part01/{slide['images'][0]}" style="width: 100%; max-height: 350px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08);">
  </div>
  <div style="flex: 1; font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
    {''.join([f'<div style="margin-bottom: 12px;">{t}</div>' for t in slide['text']])}
  </div>
</div>"""
            slide['text'] = [html]
        new_theory.append(slide)
        i += 1
        continue
    
    # 5. Handle Practice Title Slide
    if 'PRACTICE' in slide.get('text', [''])[0]:
        new_theory.append(slide)
        i += 1
        continue
        
    # 6. Handle Practice Pairs (Slide i has Image, Slide i+1 has text)
    # Wait, some slides like "PICTURE 2A" have image and text in the SAME slide (Slide 24 and 25).
    # Slide 24: PICTURE 2A (img=1 text=9)
    # Slide 27: img=1 text=0
    # Slide 28: PICTURE 01 (img=0 text=9)
    if 'PICTURE' in slide.get('text', [''])[0] and len(slide.get('images', [])) == 1:
        # Same slide has both!
        options_raw = slide['text'][1:5]
        options = [clean_text(opt)[3:] for opt in options_raw] # strip "A. "
        
        slide['practice'] = {
            "options": options,
            "answer": "A", # default to A
            "vocab": [
                {"en": "vocab 1", "vi": "nghĩa 1"},
                {"en": "vocab 2", "vi": "nghĩa 2"}
            ]
        }
        slide['text'] = []
        new_theory.append(slide)
        i += 1
        continue
        
    if len(slide.get('images', [])) == 1 and len(slide.get('text', [])) == 0:
        # It's an image slide followed by a text slide (Slide i+1)
        if i + 1 < len(dang2) and 'PICTURE' in dang2[i+1].get('text', [''])[0]:
            next_slide = dang2[i+1]
            options_raw = next_slide['text'][1:5]
            options = [clean_text(opt)[3:] for opt in options_raw]
            
            slide['practice'] = {
                "options": options,
                "answer": "A", # default
                "vocab": [
                    {"en": "vocab 1", "vi": "nghĩa 1"},
                    {"en": "vocab 2", "vi": "nghĩa 2"}
                ]
            }
            slide['text'] = []
            new_theory.append(slide)
            i += 2
            continue

    # Fallback
    new_theory.append(slide)
    i += 1

# Renumber
for idx, slide in enumerate(new_theory):
    slide['slide_index'] = idx + 1

data[2]['theory'] = new_theory
out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")
print("Restructured Dạng 2!")
