import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
json_str = content[start_idx:end_idx]

data = json.loads(json_str)

for section in data:
    if 'theory' in section:
        for slide in section['theory']:
            # Just print the first line of text for context
            t = slide.get('text', [''])[0] if slide.get('text') else ''
            print(f"Slide {slide['slide_index']}: {t[:60]}")
