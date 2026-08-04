import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

# Dạng 1 is data[1]. What is data[2]?
for idx, dang in enumerate(data):
    print(f"Index {idx}: {dang.get('title', 'No Title')} - Slides: {len(dang.get('theory', []))}")
