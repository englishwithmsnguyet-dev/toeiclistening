import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

for i, slide in enumerate(data[1]['theory']):
    idx = slide.get('slide_index')
    if idx in [87, 88, 89]:
        print(f"--- Slide {idx} ---")
        if slide['text']:
            print(slide['text'][0][:200])
        else:
            print("No text")

