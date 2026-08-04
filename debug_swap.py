import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

# The text arrays are already modified into HTML strings!
# To see the original, let's look at part01_data.json (which is unformatted).
with open('data/part01_data.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

for slide in old_data[2]['theory'][1:5]:
    if len(slide.get('images', [])) == 2:
        print(f"Slide {slide['slide_index']}:")
        for i, t in enumerate(slide['text']):
            print(f"  {i}: {t[:50]}")
