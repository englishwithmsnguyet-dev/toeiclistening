import json
import re

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

# Use image filenames to uniquely identify the slides since indices changed
slides_to_swap_by_img = [
    'slide_53_img_6.jpg', # 43
    'slide_56_img_6.jpg', # 46
    'slide_62_img_6.jpg', # 52
    'slide_88_img_6.jpg', # 79
    'slide_91_img_6.jpg', # 82
    'slide_94_img_6.jpg', # 85
    'slide_97_img_6.jpg', # 88
    'slide_100_img_6.jpg', # 91
    'slide_103_img_6.jpg'  # 94
]

for slide in data[0]['theory']:
    texts = slide.get('text', [])
    if not texts: continue
    html = texts[0]
    
    for img_marker in slides_to_swap_by_img:
        if img_marker in html:
            # We found a slide to swap!
            # Let's forcefully swap the texts
            engs = re.findall(r'<strong style="color: #00B050;">(.*?)</strong>', html)
            if len(engs) == 2:
                # We will replace engs[0] with a placeholder, engs[1] with engs[0], and placeholder with engs[1]
                # BUT wait, the Vietnamese text is also there!
                # It's much easier to just swap the image filenames!
                # If we swap the images, it's the exact same result!
                # Image 1 gets Image 2's src, and Image 2 gets Image 1's src!
                imgs = re.findall(r'src="([^"]+)"', html)
                if len(imgs) == 2:
                    new_html = html.replace(imgs[0], 'TEMP_IMG')
                    new_html = new_html.replace(imgs[1], imgs[0])
                    new_html = new_html.replace('TEMP_IMG', imgs[1])
                    slide['text'] = [new_html]
                    print(f"Swapped images for slide containing {img_marker}")
            break

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")

print("Done forcing swap.")
