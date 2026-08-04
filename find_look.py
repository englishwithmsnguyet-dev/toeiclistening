import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

for i, slide in enumerate(data[1]['theory']):
    if 'look_left.png' in str(slide):
        print(f"Look is at slide_index: {slide['slide_index']}")
        break
