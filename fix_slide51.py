import json
import re

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

for slide in data[1]['theory']:
    if slide['slide_index'] == 51:
        html = slide['text'][0]
        # Replace the first occurrence of an image with slide_62_img_bag.png
        # The left image is the first one in the HTML.
        html = re.sub(r'src="data/graphics/part01/([^"]+)"', r'src="data/graphics/part01/slide_62_img_bag.png"', html, count=1)
        slide['text'] = [html]
        print("Updated HTML for slide 51")
        break

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")
