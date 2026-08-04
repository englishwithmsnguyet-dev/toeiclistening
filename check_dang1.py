import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

# Look at Dang 1 theory slides
for slide in data[1]['theory'][:5]:
    print(f"Slide {slide.get('slide_index')}: images={slide.get('images')}")
