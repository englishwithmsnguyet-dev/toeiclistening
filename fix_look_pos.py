import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

theory = data[1]['theory']

# Find the look slide
look_idx = -1
look_slide = None
for i, slide in enumerate(theory):
    if 'look_left.png' in slide.get('images', []):
        look_idx = i
        look_slide = slide
        break

if look_slide:
    # Remove it
    theory.pop(look_idx)
    
    # Fix the double images
    look_slide['images'] = []
    
    # Find the true practice start index
    practice_idx = len(theory)
    for i, slide in enumerate(theory):
        if slide['text'] and '<details' in slide['text'][0]:
            practice_idx = i
            break
            
    # Insert look slide before practice slides
    theory.insert(practice_idx, look_slide)
    
    # Renumber all
    for i, slide in enumerate(theory):
        slide['slide_index'] = i + 1
        
    out_json = json.dumps(data, ensure_ascii=False, indent=2)
    with open('data/part01_data.js', 'w', encoding='utf-8') as f:
        f.write(f"window.part01Data = {out_json};\n")
    print("Fixed look slide position and images!")
else:
    print("Look slide not found!")
