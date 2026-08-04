import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

# Find the practice sections
for section in data:
    if 'practice' in section:
        print(f"--- Practice Section in {section.get('title')} ---")
        for i, slide in enumerate(section['practice']):
            if i < 2:
                print(f"Slide {slide.get('slide_index')}:")
                print(slide.get('text', []))
