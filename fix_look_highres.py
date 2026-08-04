import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

# The latest uploaded images are:
# Left: media__1785812082121.png
# Right: media__1785812085827.png
# But let me be safe and just replace look_left.png and look_right.png with the new ones.
# Actually I'll use new names to bust cache!

for slide in data[1]['theory']:
    if slide['slide_index'] == 94:
        html = slide['text'][0]
        html = html.replace('look_left.png', 'look_left_v2.png')
        html = html.replace('look_right.png', 'look_right_v2.png')
        slide['text'] = [html]
        print("Updated HTML for cache busting on slide 94 (look)")
        break

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")
