import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

for slide in data[1]['theory']:
    if slide['slide_index'] == 26:
        html = slide['text'][0]
        html = html.replace('slide_35_img_railing.jpg', 'slide_35_img_railing_v2.jpg')
        slide['text'] = [html]
        print("Updated HTML for cache busting on slide 26")
        break

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")
