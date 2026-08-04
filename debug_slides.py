import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

dang2 = data[2]['theory']
target_slides = [9, 11, 17, 26]

for slide in dang2:
    if slide.get('slide_index') in target_slides:
        print(f"--- Slide {slide['slide_index']} ---")
        print("Images:", slide.get('images', []))
        if slide.get('text'):
            for t in slide['text']:
                print(t[:200]) # print first 200 chars of HTML
        else:
            print("No text!")
