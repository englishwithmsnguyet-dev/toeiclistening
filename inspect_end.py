import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

theory = data[0]['theory']
for i in range(len(theory)-5, len(theory)):
    slide = theory[i]
    print(f"Slide {slide['slide_index']}:")
    print(slide['text'][0][:200] if slide['text'] else 'No text')
    print("Images:", slide.get('images', []))
