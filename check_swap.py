import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

# The index has shifted! 
# Slide 43 is now Slide 42 because Slide 37 was removed. 
# Let's search by image filename "slide_53_img_6.jpg"
for slide in data[0]['theory']:
    html = str(slide.get('text', []))
    if 'slide_53_img_6.jpg' in html:
        print(f"Slide {slide['slide_index']}:")
        print(html)
