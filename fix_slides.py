import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
json_str = content[start_idx:end_idx]

data = json.loads(json_str)

fixes = {
    14: {"left": ["adjusting a microphone", "điều chỉnh mi-crô"], "right": ["adjusting a chair", "điều chỉnh cái ghế"], "images": ["slide_14_img_5.jpg", "slide_14_img_6.png"]},
    17: {"left": ["approaching the front desk", "tiến lại gần quầy lễ tân"], "right": ["approaching the cash register", "tiến lại gần quầy tính tiền"], "images": ["slide_17_img_6.jpg", "slide_17_img_7.jpg"]},
    20: {"left": ["carrying a briefcase", "mang cặp tài liệu"], "right": ["carrying a jacket", "mang chiếc áo khoác"], "images": ["slide_20_img_6.jpg", "slide_20_img_7.jpg"]},
    23: {"left": ["checking a schedule", "kiểm tra lịch làm việc"], "right": ["checking documents", "kiểm tra tài liệu"], "images": ["slide_23_img_6.jpg", "slide_23_img_7.jpg"]},
    26: {"left": ["entering an amusement park", "tiến vào công viên giải trí"], "right": ["entering a building", "tiến vào toà nhà"], "images": ["slide_26_img_6.jpg", "slide_26_img_7.jpg"]},
    29: {"left": ["hanging a picture", "treo một bức tranh"], "right": ["hanging a clock", "treo một chiếc đồng hồ"], "images": ["slide_29_img_6.jpg", "slide_29_img_7.jpg"]},
    32: {"left": ["holding a book", "cầm một cuốn sách"], "right": ["holding a pen", "cầm một chiếc bút"], "images": ["slide_32_img_6.jpg", "slide_32_img_7.jpg"]},
    35: {"left": ["leaning against the wall", "tựa vào bức tường"], "right": ["leaning against the railing", "tựa vào lan can"], "images": ["slide_35_img_6.jpg", "slide_35_img_7.png"]},
    38: {"left": ["looking at a monitor", "nhìn vào màn hình"], "right": ["looking at a map", "nhìn vào bản đồ"], "images": ["slide_38_img_6.jpg", "slide_38_img_7.jpg"]},
    41: {"left": ["reaching for a book", "với lấy một cuốn sách"], "right": ["reaching for an item", "với lấy một món đồ"], "images": ["slide_41_img_6.jpg", "slide_41_img_7.jpg"]}
}

for section in data:
    if 'theory' in section:
        for slide in section['theory']:
            if slide.get('slide_index') in fixes:
                fix = fixes[slide['slide_index']]
                
                # Render left/right texts
                # The first item is English, the second is Vietnamese
                
                def render_text(items):
                    html_parts = []
                    for i, t in enumerate(items):
                        if i == 0:
                            # English phrase: Bold and green (#00B050)
                            html_parts.append(f'<div style="margin-bottom: 8px;"><strong style="color: #00B050;">{t}</strong></div>')
                        else:
                            # Vietnamese: Normal text
                            html_parts.append(f'<div style="margin-bottom: 8px;">{t}</div>')
                    return "".join(html_parts)

                left_html = render_text(fix["left"])
                right_html = render_text(fix["right"])
                
                html = f'''<div style="display: flex; flex-direction: row; gap: 32px; justify-content: center; width: 100%; align-items: flex-start; margin-top: 10px;">
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/{fix["images"][0]}" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      {left_html}
    </div>
  </div>
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/{fix["images"][1]}" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      {right_html}
    </div>
  </div>
</div>'''
                slide['text'] = [html]
                slide['images'] = []

# Serialize back
out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")

print("Successfully updated part01_data.js using Python")
