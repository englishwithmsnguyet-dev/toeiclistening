import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

theory = data[1]['theory']
for slide in theory:
    if slide['slide_index'] >= 96:
        print(f"--- Slide {slide['slide_index']} ---")
        for idx, t in enumerate(slide['text']):
            print(f"[{idx}] {t}")
