import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('[')
end = content.rfind(']')+1
data = json.loads(content[start:end])

for s in data:
    if s.get('type') == 'test':
        print(f"Found test: id={s.get('id')}, title={s.get('title')}")
