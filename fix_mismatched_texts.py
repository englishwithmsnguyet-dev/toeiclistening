import json
import re

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
json_str = content[start_idx:end_idx]

data = json.loads(json_str)

for section in data:
    if 'theory' in section:
        for slide in section['theory']:
            texts = slide.get('text', [])
            if not texts: continue
            
            html = texts[0]
            
            if 'hanging a picture' in html and 'hanging a clock' in html:
                # Fix Slide 20
                html = html.replace('hanging a picture', 'hanging a sign')
                html = html.replace('treo một bức tranh', 'treo một biển hiệu')
                html = html.replace('hanging a clock', 'hanging a jacket')
                html = html.replace('treo một chiếc đồng hồ', 'treo một chiếc áo khoác')
                slide['text'] = [html]
                print(f"Fixed Slide {slide['slide_index']}: hanging a picture -> hanging a sign")
                
            elif 'holding a book' in html and 'holding a pen' in html:
                # Fix Slide 23
                html = html.replace('holding a book', 'holding a stack of folders')
                html = html.replace('cầm một cuốn sách', 'cầm một tập tài liệu')
                html = html.replace('holding a pen', 'holding a handrail')
                html = html.replace('cầm một chiếc bút', 'cầm một tay vịn')
                slide['text'] = [html]
                print(f"Fixed Slide {slide['slide_index']}: holding a book -> holding a stack of folders")

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")

print("Done fixing mismatched texts.")
