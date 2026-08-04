import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

dang2 = data[2]['theory']

# Let's print out a few slides to see what they look like
print("--- Dạng 2 First 3 Slides ---")
for slide in dang2[:3]:
    print(f"Slide {slide['slide_index']}:")
    print(f"Images: {slide['images']}")
    for i, t in enumerate(slide['text']):
        print(f"  Text {i}: {t[:100]}")

print("\n--- Dạng 2 Last 6 Slides (Practice?) ---")
for slide in dang2[-6:]:
    print(f"Slide {slide['slide_index']}:")
    print(f"Images: {slide['images']}")
    for i, t in enumerate(slide['text']):
        print(f"  Text {i}: {t[:100]}")

