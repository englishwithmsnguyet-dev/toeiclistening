import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

for slide in data[1]['theory']:
    if slide['slide_index'] == 89:
        html = slide['text'][0]
        html = html.replace('slide_100_img_7.jpg', 'slide_100_img_fold_fixed.png')
        html = html.replace('folding a towel', 'folding some clothes')
        html = html.replace('gấp khăn', 'gấp quần áo')
        
        # also replace the right side just in case it was also wrong? 
        # I'll leave the right side alone unless told otherwise, but it might be weird to have jeans and a blanket.
        # Actually I'll replace the right image with the same image and text "folding a garment" just to be safe.
        # Let's just fix the left side.
        
        slide['text'] = [html]
        print("Updated fold slide (89)")
        break

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")
