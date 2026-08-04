import json
import re

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

theory = data[1]['theory']
for slide in theory:
    if slide['slide_index'] >= 96 and slide['slide_index'] <= 101:
        text_arr = slide.get('text', [])
        if len(text_arr) < 5: continue
        
        # We assume 1-4 are A, B, C, D
        # 0, 5, 6, 7 are vietnamese vocab
        vocab = []
        options = []
        for i, t in enumerate(text_arr):
            # Clean up the text a bit
            if i in [1, 2, 3, 4]:
                options.append(t)
            else:
                # Remove spans to just get the raw text for vocab
                v = re.sub(r'<[^>]+>', '', t).strip()
                if v:
                    vocab.append(v)
        
        # Build HTML
        html = '''<div style="display: flex; flex-direction: column; align-items: center; justify-content: flex-start; gap: 20px; width: 100%;">
  <div style="display: flex; flex-direction: column; gap: 12px; font-size: 1.3rem; line-height: 1.8; color: var(--text-main); text-align: left; background: #fff; padding: 24px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); width: 100%; max-width: 800px;">'''
        
        for opt in options:
            html += f'\n    <div>{opt}</div>'
            
        if vocab:
            html += '''\n    <details style="margin-top: 16px; cursor: pointer;">
      <summary style="font-weight: bold; color: #16a34a; outline: none; list-style-type: '👉 ';">Hiển thị từ vựng</summary>
      <div style="margin-top: 12px; display: flex; flex-wrap: wrap; gap: 12px;">'''
            for v in vocab:
                html += f'\n        <span style="background: #f0fdf4; padding: 6px 16px; border-radius: 99px; font-size: 1.1rem; color: #15803d; border: 1px solid #bbf7d0;">{v}</span>'
            html += '\n      </div>\n    </details>'
            
        html += '\n  </div>\n</div>'
        
        slide['text'] = [html]
        print(f"Formatted Slide {slide['slide_index']}")

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")

print("Done formatting practice slides.")
