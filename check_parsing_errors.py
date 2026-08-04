import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

slides_to_check = [40, 43, 46, 49]
for section in data:
    if 'theory' in section:
        for s in section['theory']:
            if s['slide_index'] in slides_to_check:
                print(f"--- Slide {s['slide_index']} ---")
                print(s['text'][0])
