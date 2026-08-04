import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('[')
end = content.rfind(']')+1
data = json.loads(content[start:end])
theory = data[2]['theory']

# Create the new Structure Slide HTML
html = """<div style="text-align: center; margin-bottom: 32px;"><span style="color: #FF0000; font-size: 2.2rem; font-weight: bold; text-transform: uppercase;">CẤU TRÚC</span></div>
<div style="display: flex; justify-content: center; align-items: center; gap: 12px; margin-bottom: 40px; flex-wrap: wrap;"><div style="background: #eff6ff; border: 2px solid #3b82f6; border-radius: 8px; padding: 12px 24px; font-size: 1.8rem; font-weight: bold; color: #1d4ed8;">Subject</div><div style="font-size: 2rem; font-weight: bold; color: #94a3b8;">+</div><div style="background: #f0fdf4; border: 2px solid #22c55e; border-radius: 8px; padding: 12px 24px; font-size: 1.8rem; font-weight: bold; color: #15803d;">are + V-ing</div><div style="font-size: 2rem; font-weight: bold; color: #94a3b8;">+</div><div style="background: #fdf4ff; border: 2px solid #d946ef; border-radius: 8px; padding: 12px 24px; font-size: 1.8rem; font-weight: bold; color: #a21caf;">Object</div></div>
<div style="max-width: 800px; margin: 0 auto; text-align: left; background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);"><div style="margin-bottom: 16px; font-size: 1.3rem;">
    <span style="color: #1d4ed8; font-weight: bold; min-width: 120px; display: inline-block;">Subject (S):</span>
    <span style="color: #334155;">They, The men, The women, The people, Some people</span>
</div><div style="margin-bottom: 16px; font-size: 1.3rem;">
    <div style="color: #1d4ed8; font-weight: bold; margin-bottom: 8px;">Lưu ý viết tắt:</div>
    <ul style="color: #334155; margin: 0; padding-left: 24px; line-height: 1.8;">
        <li>They are &rarr; <strong>They're</strong></li>
        <li>(Chú ý người bản ngữ thường đọc lướt chữ "are" trong các câu TOEIC Listening)</li>
    </ul>
</div></div>"""

new_slide = {
    "slide_index": 2, # Will be renumbered
    "text": [html],
    "images": []
}

# Insert it at index 1 (right after TRANH CÓ NHIỀU NGƯỜI)
theory.insert(1, new_slide)

# Renumber all slides in dang 2
for idx, s in enumerate(theory):
    s['slide_index'] = idx + 1

data[2]['theory'] = theory

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")

print("Added Dạng 2 Structure Slide successfully!")
