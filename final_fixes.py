import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
json_str = content[start_idx:end_idx]

data = json.loads(json_str)

for section in data:
    if 'theory' in section:
        theory = section['theory']
        
        # 1 & 2: Fix missing images
        for slide in theory:
            if slide.get('text') and 'stand' in slide['text'][0] and '/stænd/' in str(slide['text']) and slide['slide_index'] < 110:
                slide['images'] = ["slide_63_img_3.jpg"]
            if slide.get('text') and 'fold' in slide['text'][0] and '/fəʊld/' in str(slide['text']) and slide['slide_index'] < 110:
                slide['images'] = ["slide_89_img_3.jpg"]
                
            # 3: Fix Slide 79 (wearing a long-sleeved shirt / wearing sunglasses)
            if 'wearing a long-sleeved shirt' in str(slide.get('text')):
                # apply flexbox
                html = '''<div style="display: flex; flex-direction: row; gap: 32px; justify-content: center; width: 100%; align-items: flex-start; margin-top: 10px;">
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/slide_88_img_6.jpg" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">wearing a long-sleeved shirt</strong></div><div style="margin-bottom: 8px;">mặc áo sơ mi dài tay</div>
    </div>
  </div>
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/slide_88_img_7.jpg" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">wearing sunglasses</strong></div><div style="margin-bottom: 8px;">đeo kính râm</div>
    </div>
  </div>
</div>'''
                slide['text'] = [html]
                slide['images'] = []
                
        # 4: Move "looking at a monitor / looking at a map"
        slide_to_move_idx = -1
        dest_idx = -1
        
        for i, slide in enumerate(theory):
            if 'looking at a monitor' in str(slide.get('text')):
                slide_to_move_idx = i
            elif 'looking into a copy machine' in str(slide.get('text')):
                dest_idx = i
                
        if slide_to_move_idx != -1 and dest_idx != -1:
            slide_to_move = theory.pop(slide_to_move_idx)
            if dest_idx > slide_to_move_idx:
                dest_idx -= 1
            theory.insert(dest_idx + 1, slide_to_move)
            
        # Renumber
        for i, slide in enumerate(theory):
            slide['slide_index'] = i + 1

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")

print("Fixed missing images, fixed Slide 79 layout, and moved looking at a monitor slide.")
