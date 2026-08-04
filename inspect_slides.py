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
            if len(slide.get('images', [])) == 2:
                print(f"Slide {slide['slide_index']}:")
                print(f"  Images: {slide['images']}")
                print(f"  Text count: {len(slide.get('text', []))}")
                for i, t in enumerate(slide.get('text', [])):
                    print(f"    {i}: {t}")
