import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
json_str = content[start_idx:end_idx]

data = json.loads(json_str)

for section in data:
    if 'theory' in section:
        for slide in section['theory']:
            idx = slide.get('slide_index')
            
            # Slide 30: hold
            if idx == 30:
                slide['images'] = ["slide_30_img_hold.png"]
                
            # Slide 33: lean
            elif idx == 33:
                slide['images'] = ["slide_33_img_lean.png"]
                
            # Slide 39: look
            elif idx == 39:
                slide['images'] = ["slide_39_img_look.png"]
                
            # Slide 35: replace the image name in the html
            elif idx == 35:
                if len(slide['text']) > 0:
                    slide['text'][0] = slide['text'][0].replace('slide_35_img_6.jpg', 'slide_35_img_6_new.png')
            
            # Slide 62: reaching into a bag / reaching for a telephone
            elif idx == 62:
                # This is a multiple image slide that was NOT formatted by fix_slides.py previously.
                # Let's format it nicely!
                html = '''<div style="display: flex; flex-direction: row; gap: 32px; justify-content: center; width: 100%; align-items: flex-start; margin-top: 10px;">
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/slide_62_img_6.jpg" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">reaching into a bag</strong></div><div style="margin-bottom: 8px;">với tay vào trong túi</div>
    </div>
  </div>
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/slide_62_img_7.png" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style=\"font-size: 1.3rem; line-height: 1.8; color: var(--text-main);\">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">reaching for a telephone</strong></div><div style="margin-bottom: 8px;">với tay tới cái điện thoại</div>
    </div>
  </div>
</div>'''
                slide['text'] = [html]
                slide['images'] = []

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")

print("Successfully linked all missing images.")
