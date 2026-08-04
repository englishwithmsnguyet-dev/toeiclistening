import json
with open('data/part01_data.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

for slide in old_data[2]['theory']:
    if slide.get('slide_index') == 121: # wait, indices were renumbered. Slide 11 was at index 10 in dang2_raw.
        pass

for i, slide in enumerate(old_data[2]['theory']):
    if i in [8, 10, 16, 25]: # 9, 11, 17, 26 after renumbering? Wait, renumbering shifted things.
        print(f"--- Index {i} Original ---")
        print("Images:", slide.get('images', []))
        print("Text len:", len(slide.get('text', [])))
        for t in slide.get('text', []):
            print(t[:100])
