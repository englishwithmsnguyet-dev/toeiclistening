import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
json_str = content[start_idx:end_idx]

data = json.loads(json_str)

def make_formula(title, blocks, annotations):
    blocks_html = []
    for i, b in enumerate(blocks):
        bg, border, color, text = b
        blocks_html.append(f'<div style="background: {bg}; border: 2px solid {border}; border-radius: 8px; padding: 12px 24px; font-size: 1.8rem; font-weight: bold; color: {color};">{text}</div>')
        if i < len(blocks) - 1:
            blocks_html.append('<div style="font-size: 2rem; font-weight: bold; color: #94a3b8;">+</div>')
    
    formula_html = f'<div style="display: flex; justify-content: center; align-items: center; gap: 12px; margin-bottom: 40px; flex-wrap: wrap;">{"".join(blocks_html)}</div>'
    
    ann_html = []
    for ann in annotations:
        label, val = ann
        ann_html.append(f'''<div style="margin-bottom: 16px; font-size: 1.3rem;">
    <span style="color: #1d4ed8; font-weight: bold; min-width: 120px; display: inline-block;">{label}</span>
    <span style="color: #334155;">{val}</span>
</div>''')
    
    ann_container = f'<div style="max-width: 800px; margin: 0 auto; text-align: left; background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">{"".join(ann_html)}</div>'
    
    return f'<div style="text-align: center; margin-bottom: 32px;"><span style="color: #FF0000; font-size: 2.2rem; font-weight: bold; text-transform: uppercase;">{title}</span></div>\n{formula_html}\n{ann_container}'


for section in data:
    if 'theory' in section:
        for slide in section['theory']:
            idx = slide.get('slide_index')
            
            if idx == 11:
                blocks = [
                    ("#eff6ff", "#3b82f6", "#1d4ed8", "Subject"),
                    ("#f0fdf4", "#22c55e", "#15803d", "is + V-ing"),
                    ("#fdf4ff", "#d946ef", "#a21caf", "Object")
                ]
                annotations = [
                    ("Subject (S):", "He, She, The man, The woman"),
                    ("Lưu ý viết tắt:", "He is &rarr; <strong>He's</strong> &nbsp; | &nbsp; She is &rarr; <strong>She's</strong>")
                ]
                slide['text'] = [make_formula("CẤU TRÚC", blocks, annotations)]
                
            elif idx == 47:
                blocks = [
                    ("#eff6ff", "#3b82f6", "#1d4ed8", "Subject"),
                    ("#f0fdf4", "#22c55e", "#15803d", "are + V-ing"),
                    ("#fdf4ff", "#d946ef", "#a21caf", "Object")
                ]
                annotations = [
                    ("Subject (S):", "They, The men, The women"),
                    ("Lưu ý viết tắt:", "They are &rarr; <strong>They're</strong>")
                ]
                slide['text'] = [make_formula("CẤU TRÚC", blocks, annotations)]
                
            elif idx == 114:
                blocks = [
                    ("#eff6ff", "#3b82f6", "#1d4ed8", "Subject"),
                    ("#f0fdf4", "#22c55e", "#15803d", "is/are + being + V3/ed"),
                    ("#fdf4ff", "#d946ef", "#a21caf", "by (Object)")
                ]
                annotations = [
                    ("Ý nghĩa:", "Sự việc <strong>đang được (ai đó) làm gì</strong>")
                ]
                slide['text'] = [make_formula("CẤU TRÚC CHÍNH", blocks, annotations)]
                
            elif idx == 148:
                blocks = [
                    ("#eff6ff", "#3b82f6", "#1d4ed8", "Subject"),
                    ("#f0fdf4", "#22c55e", "#15803d", "have/has + been + V3/ed")
                ]
                annotations = [
                    ("Ý nghĩa:", "Sự việc <strong>đã được hoàn thành</strong>")
                ]
                slide['text'] = [make_formula("CẤU TRÚC CHÍNH", blocks, annotations)]

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")

print("Updated grammar layouts perfectly")
