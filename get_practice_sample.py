import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

# Find the first practice slide
for slide in data[1]['theory']:
    if slide['text'] and isinstance(slide['text'], list) and len(slide['text']) > 0:
        if '<details' in str(slide['text'][0]):
            print(slide)
            break
