import json
with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()
start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])
theory = data[0]['theory']
print(f"Total slides in DANG 1: {len(theory)}")
for i, s in enumerate(theory):
    print(f"Index {i}: Slide {s['slide_index']}")
