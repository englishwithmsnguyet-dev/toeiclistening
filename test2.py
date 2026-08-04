import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

found = False
for slide in data[0]['theory']:
    html = str(slide.get('text', []))
    if 'slide_53_img_6.jpg' in html:
        print("Found slide!")
        found = True
        import re
        engs = re.findall(r'<strong style="color: #00B050;">(.*?)</strong>', html)
        print("Engs:", engs)
        imgs = re.findall(r'src="([^"]+)"', html)
        print("Imgs:", imgs)

if not found: print("Not found in theory!")
