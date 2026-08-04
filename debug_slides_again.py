import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

dang2 = data[2]['theory']

for slide in dang2:
    idx = slide.get('slide_index')
    if idx in [9, 11, 17, 26]:
        print(f"\n--- Slide {idx} ---")
        print("Images:", slide.get('images', []))
        if slide.get('text'):
            for t in slide['text']:
                print(t[:200]) # print first 200 chars
        else:
            print("No text!")
