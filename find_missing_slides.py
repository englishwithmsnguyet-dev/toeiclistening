import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
json_str = content[start_idx:end_idx]
data = json.loads(json_str)

terms = [
    "hold", "lean", "leaning against the wall", "look", 
    "reaching for a telephone", "reaching into a bag"
]

for section in data:
    if 'theory' in section:
        for slide in section['theory']:
            text = " ".join(slide.get('text', []))
            for term in terms:
                if term.lower() in text.lower() or term.lower() in text.replace('>', '').replace('<', '').lower():
                    print(f"Slide {slide['slide_index']}: Found term '{term}'")
                    print(f"  Images array: {slide.get('images', [])}")

