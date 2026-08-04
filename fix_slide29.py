import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

new_html = '''<div style="display: flex; flex-direction: row; gap: 32px; justify-content: center; width: 100%; align-items: flex-start; margin-top: 10px;">
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/slide_38_img_7.jpg" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">loading some boxes onto a shopping cart</strong></div><div style="margin-bottom: 8px;">chất thùng lên xe đẩy hàng</div>
    </div>
  </div>
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/slide_38_img_6.jpg" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">loading the cargo onto the plane</strong></div><div style="margin-bottom: 8px;">chất hàng hoá lên trên máy bay</div>
    </div>
  </div>
</div>'''

for slide in data[1]['theory']:
    if slide['slide_index'] == 29:
        slide['text'] = [new_html]
        print("Updated Slide 29 layout perfectly!")
        break

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")

