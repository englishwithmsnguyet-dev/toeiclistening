import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()
start = content.find('[')
end = content.rfind(']')+1
data = json.loads(content[start:end])

theory = data[2]['theory']
for s in theory:
    if s.get('practice'):
        print(f"Slide {s['slide_index']}: Answer currently is {s['practice']['answer']}")
