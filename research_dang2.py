import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

dang2 = data[2]['theory']
# I want to dump the text arrays of the theory slides (Slide 2-25)
print("--- Theory Slides ---")
for slide in dang2[2:10]:
    print(f"Slide {slide.get('slide_index')}:")
    print("Images:", slide.get('images', []))
    print("Text:", slide.get('text', []))

print("\n--- Practice Slides ---")
for slide in dang2[-6:]:
    print(f"Slide {slide.get('slide_index')}:")
    print("Images:", slide.get('images', []))
    print("Text:", slide.get('text', []))
