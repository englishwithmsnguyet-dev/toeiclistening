import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

for i, section in enumerate(data):
    title = section.get('title', 'NO TITLE')
    num_theory = len(section.get('theory', []))
    num_practice = len(section.get('practice', []))
    print(f"[{i}] {title}: theory={num_theory}, practice={num_practice}")
