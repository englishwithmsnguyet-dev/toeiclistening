import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
json_str = content[start_idx:end_idx]

data = json.loads(json_str)

html_template = """<div style="text-align: center; margin-bottom: 24px;"><span style="color: #FF0000; font-size: 2rem; font-weight: bold; text-transform: uppercase;">{title}</span></div>
<div style="display: flex; justify-content: center; align-items: stretch; gap: 16px; margin: 0 auto; max-width: 1000px; text-align: center; flex-wrap: wrap;">
{blocks}
</div>"""

def make_block(title, items, color, border, bg):
    items_html = "".join([f'<div>{item}</div>' for item in items])
    return f"""    <div style="flex: 1; min-width: 200px; background: {bg}; border: 2px solid {border}; border-radius: 8px; padding: 20px; display: flex; flex-direction: column;">
        <div style="font-size: 1.6rem; font-weight: bold; color: {color}; border-bottom: 2px solid {border}; padding-bottom: 12px; margin-bottom: 12px;">{title}</div>
        <div style="font-size: 1.4rem; line-height: 1.8; color: #334155; flex-grow: 1; display: flex; flex-direction: column; justify-content: center;">
            {items_html}
        </div>
    </div>"""

def make_plus():
    return f"""    <div style="display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: bold; color: #94a3b8; padding: 0 8px;">+</div>"""

def make_arrow():
    return f"""    <div style="display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: bold; color: #94a3b8; padding: 0 8px;">&rarr;</div>"""


for section in data:
    if 'theory' in section:
        for slide in section['theory']:
            # Slide 11
            if slide.get('slide_index') == 11:
                b1 = make_block("Subject", ["He", "The man", "She", "The woman"], "#1d4ed8", "#bfdbfe", "#eff6ff")
                b2 = make_block("is + V-ing", [""], "#15803d", "#bbf7d0", "#f0fdf4")
                b3 = make_block("Object", [""], "#a21caf", "#f5d0fe", "#fdf4ff")
                blocks = b1 + "\n" + make_plus() + "\n" + b2 + "\n" + make_plus() + "\n" + b3
                slide['text'] = [html_template.format(title="CẤU TRÚC", blocks=blocks)]
                
            # Slide 47
            elif slide.get('slide_index') == 47:
                b1 = make_block("Subject", ["They", "The men", "The women"], "#1d4ed8", "#bfdbfe", "#eff6ff")
                b2 = make_block("are + V-ing", [""], "#15803d", "#bbf7d0", "#f0fdf4")
                b3 = make_block("Object", [""], "#a21caf", "#f5d0fe", "#fdf4ff")
                blocks = b1 + "\n" + make_plus() + "\n" + b2 + "\n" + make_plus() + "\n" + b3
                slide['text'] = [html_template.format(title="CẤU TRÚC", blocks=blocks)]
                
            # Slide 114
            elif slide.get('slide_index') == 114:
                b1 = make_block("Subject", ["(Sự việc)"], "#1d4ed8", "#bfdbfe", "#eff6ff")
                b2 = make_block("is/are + being + V3/ed", ["(đang được làm gì)"], "#15803d", "#bbf7d0", "#f0fdf4")
                b3 = make_block("by (Object)", ["(bởi ai đó)"], "#a21caf", "#f5d0fe", "#fdf4ff")
                blocks = b1 + "\n" + make_plus() + "\n" + b2 + "\n" + make_plus() + "\n" + b3
                slide['text'] = [html_template.format(title="CẤU TRÚC CHÍNH", blocks=blocks)]
                
            # Slide 148
            elif slide.get('slide_index') == 148:
                b1 = make_block("Subject", ["(Sự việc)"], "#1d4ed8", "#bfdbfe", "#eff6ff")
                b2 = make_block("have/has + been + V3/ed", ["(đã được hoàn thành)"], "#15803d", "#bbf7d0", "#f0fdf4")
                blocks = b1 + "\n" + make_plus() + "\n" + b2
                slide['text'] = [html_template.format(title="CẤU TRÚC CHÍNH", blocks=blocks)]


out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")

print("Successfully updated grammar slides")
