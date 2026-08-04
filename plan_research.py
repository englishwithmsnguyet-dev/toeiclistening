import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()
    
start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

slides_to_check = [20, 26, 29, 37, 40, 43, 46, 49, 52, 53, 79, 82, 85, 88, 89, 91, 94]
for slide_idx in slides_to_check:
    for section in data:
        if 'theory' in section:
            for s in section['theory']:
                if s['slide_index'] == slide_idx:
                    print(f"--- Slide {slide_idx} ---")
                    print(s['text'][0][:150] if s['text'] else "No text")
                    print(f"Images: {s.get('images', [])}")

# Look for look, pay for, talk
for section in data:
    if 'theory' in section:
        for s in section['theory']:
            idx = s['slide_index']
            t = str(s['text'])
            if 'look ' in t or 'look<' in t:
                print(f"look slide: {idx}")
            if 'pay for' in t:
                print(f"pay for slide: {idx}")
            if 'talk' in t:
                print(f"talk slide: {idx}")
