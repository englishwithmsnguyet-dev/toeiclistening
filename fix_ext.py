import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

# Since Slide 37 was moved and 53 was deleted, Slide 26 might be at a slightly different index, 
# but we already renumbered everything in the last script! So it should still be Slide 26.
for slide in data[1]['theory']:
    if slide['slide_index'] == 26:
        html = slide['text'][0]
        html = html.replace('slide_35_img_7.png', 'slide_35_img_7.jpg')
        slide['text'] = [html]
        print("Fixed image extension on slide 26")
        
out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")
print("Done fixing extension.")
