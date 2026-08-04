import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

look_html = '''<div style="display: flex; flex-direction: row; gap: 32px; justify-content: center; width: 100%; align-items: flex-start; margin-top: 10px;">
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/look_left.png" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">looking at merchandise on display</strong></div><div style="margin-bottom: 8px;">nhìn vào hàng hoá được trưng bày</div>
    </div>
  </div>
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/look_right.png" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">looking in a display case</strong></div><div style="margin-bottom: 8px;">nhìn vào tủ trưng bày</div>
    </div>
  </div>
</div>'''

new_slide = {
    "slide_index": -1, # will be updated
    "text": [look_html],
    "images": ["look_left.png", "look_right.png"],
    "audio": None
}

# We want to insert it before the practice slides.
# Practice slides in DANG 1 start when text is simple arrays (no <div> wrapper)
# But it's easier to just insert it at index 95.
theory = data[1]['theory']
# Find the first practice slide (the one that has "xe đẩy hàng" in text)
practice_start_idx = len(theory)
for i, slide in enumerate(theory):
    if slide['text'] and isinstance(slide['text'], list):
        if 'xe đẩy hàng' in slide['text'][0] or 'xe đẩy hàng' in str(slide['text']):
            practice_start_idx = i
            break

theory.insert(practice_start_idx, new_slide)

# Renumber all slides in DANG 1
for i, slide in enumerate(theory):
    slide['slide_index'] = i + 1

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")

print(f"Added look slide. New total slides in DANG 1: {len(theory)}")
