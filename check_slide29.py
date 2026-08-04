import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

for slide in data[1]['theory']:
    if slide['slide_index'] == 29:
        print("Slide 29 Text:", slide['text'][0][:150])
        print("Images:", slide['images'])
        break
