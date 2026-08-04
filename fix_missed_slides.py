import json
import re

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

# The theory slides are in data[1]['theory']
theory = data[1]['theory']
for slide in theory:
    if slide['slide_index'] == 20:
        html = slide['text'][0]
        html = html.replace('hanging a sign', 'hanging a sign on the wall')
        html = html.replace('treo một biển hiệu', 'treo biển hiệu trên tường')
        html = html.replace('hanging a jacket', 'hanging a jacket on a coat rack')
        html = html.replace('treo một chiếc áo khoác', 'treo áo khoác lên giá')
        slide['text'] = [html]
        print("Fixed slide 20")
    
    elif slide['slide_index'] == 26:
        html = slide['text'][0]
        html = html.replace('leaning against the wall', 'leaning against a car')
        html = html.replace('tựa vào bức tường', 'tựa vào chiếc xe hơi')
        slide['text'] = [html]
        print("Fixed slide 26")
        # Also print the image src to see if it's broken
        imgs = re.findall(r'src="([^"]+)"', html)
        print("Images in 26:", imgs)
        
    elif slide['slide_index'] == 40:
        html = f'''<div style="display: flex; flex-direction: row; gap: 32px; justify-content: center; width: 100%; align-items: flex-start; margin-top: 10px;">
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/slide_50_img_6.jpg" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">pouring water into a cup</strong></div><div style="margin-bottom: 8px;">rót nước vào cốc</div>
    </div>
  </div>
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/slide_50_img_7.jpg" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">pouring liquid into a glass</strong></div><div style="margin-bottom: 8px;">rót chất lỏng vào ly</div>
    </div>
  </div>
</div>'''
        slide['text'] = [html]
        print("Fixed slide 40")
        
    elif slide['slide_index'] == 49:
        html = f'''<div style="display: flex; flex-direction: row; gap: 32px; justify-content: center; width: 100%; align-items: flex-start; margin-top: 10px;">
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/slide_59_img_6.jpg" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">putting merchandise into a bag</strong></div><div style="margin-bottom: 8px;">bỏ hàng hoá vào túi</div>
    </div>
  </div>
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/slide_59_img_7.png" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">putting items in a backpack</strong></div><div style="margin-bottom: 8px;">bỏ đồ đạc vào ba lô</div>
    </div>
  </div>
</div>'''
        slide['text'] = [html]
        print("Fixed slide 49")

# Also delete slide 53
slide_53_obj = None
for s in data[1]['theory']:
    if s['slide_index'] == 53:
        slide_53_obj = s
        break
if slide_53_obj:
    data[1]['theory'].remove(slide_53_obj)
    print("Deleted slide 53")

# Move slide 37 from DANG 1 to DANG 2
slide_37_obj = None
for s in data[1]['theory']:
    if s['slide_index'] == 37:
        slide_37_obj = s
        break
if slide_37_obj:
    data[1]['theory'].remove(slide_37_obj)
    data[2]['theory'].insert(1, slide_37_obj)
    print("Moved slide 37")

# Renumber DANG 1
for i, slide in enumerate(data[1]['theory']):
    slide['slide_index'] = i + 1

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")
print("Done fixing missed slides.")
