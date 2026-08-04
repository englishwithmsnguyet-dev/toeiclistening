import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

theory = data[1]['theory']

pay_html = '''<div style="display: flex; flex-direction: row; gap: 32px; justify-content: center; width: 100%; align-items: flex-start; margin-top: 10px;">
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/pay_left.png" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">paying for a meal</strong></div><div style="margin-bottom: 8px;">thanh toán bữa ăn</div>
    </div>
  </div>
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/pay_right.png" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">paying for merchandise</strong></div><div style="margin-bottom: 8px;">thanh toán hàng hoá</div>
    </div>
  </div>
</div>'''

new_slide = {
    "slide_index": -1, # will be updated
    "text": [pay_html],
    "images": [],
    "audio": None
}

# Find look slide
look_idx = -1
for i, slide in enumerate(theory):
    if 'look_left_v2.png' in str(slide):
        look_idx = i
        break

if look_idx != -1:
    theory.insert(look_idx, new_slide)
else:
    theory.append(new_slide)

# Renumber all
for i, slide in enumerate(theory):
    slide['slide_index'] = i + 1

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")
print(f"Added pay for slide! New total DANG 1 slides: {len(theory)}")
