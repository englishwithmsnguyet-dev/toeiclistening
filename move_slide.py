import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
json_str = content[start_idx:end_idx]

data = json.loads(json_str)

for section in data:
    if 'theory' in section:
        theory = section['theory']
        
        # Find slide 41 and slide 62
        slide_41_idx = -1
        slide_62_idx = -1
        
        for i, slide in enumerate(theory):
            if slide['slide_index'] == 41:
                slide_41_idx = i
            elif slide['slide_index'] == 62:
                slide_62_idx = i
                
        if slide_41_idx != -1 and slide_62_idx != -1:
            # Pop slide 41
            slide_41 = theory.pop(slide_41_idx)
            
            # Recalculate slide 62 index after popping (it will shift if 62 > 41)
            if slide_62_idx > slide_41_idx:
                slide_62_idx -= 1
                
            # Insert slide 41 after slide 62
            theory.insert(slide_62_idx + 1, slide_41)
            
            # Renumber all slides sequentially starting from 1
            for i, slide in enumerate(theory):
                slide['slide_index'] = i + 1
                
out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")

print("Slide 41 moved after Slide 62 and renumbered successfully.")
