import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])
theory = data[1]['theory']

# 1. Extract look and pay for slides
look_slide = None
pay_slide = None

for slide in list(theory):
    if 'look_left_v2.png' in str(slide):
        look_slide = slide
        theory.remove(slide)
    elif 'pay_left.png' in str(slide):
        pay_slide = slide
        theory.remove(slide)

# 2. Fix Slide 26
for slide in theory:
    if 'leaning on a railing' in str(slide['text']):
        html = slide['text'][0]
        html = html.replace('slide_35_img_railing_v2.jpg', 'slide_35_img_railing_v3.jpg')
        slide['text'] = [html]
        break

# 3. Revert Slide 89 and fix Slide 87
# (Wait, if I removed two slides, their indices are no longer 87/89. Let's find them by content)
for slide in theory:
    if slide['text'] and isinstance(slide['text'], list):
        # The modified Slide 89
        if 'folding some clothes' in str(slide['text'][0]):
            html = slide['text'][0]
            html = html.replace('slide_100_img_fold_fixed.png', 'slide_100_img_7.jpg')
            html = html.replace('folding some clothes', 'folding a towel')
            html = html.replace('gấp quần áo', 'gấp khăn')
            slide['text'] = [html]
        
        # The original Slide 87 title slide
        elif '<strong>fold</strong>' in slide['text'][0]:
            slide['images'] = ['slide_100_img_fold_fixed.png']

# 4. Insert look slide after "looking at the monitor"
look_target_idx = -1
for i, slide in enumerate(theory):
    if 'looking at' in str(slide['text']) and 'the monitor' in str(slide['text']):
        look_target_idx = i
        break
if look_target_idx != -1 and look_slide:
    theory.insert(look_target_idx + 1, look_slide)

# 5. Insert pay for slide after "paying for a purchase"
pay_target_idx = -1
for i, slide in enumerate(theory):
    if 'paying for' in str(slide['text']) and 'a purchase' in str(slide['text']):
        pay_target_idx = i
        break
if pay_target_idx != -1 and pay_slide:
    theory.insert(pay_target_idx + 1, pay_slide)

# Renumber all
for i, slide in enumerate(theory):
    slide['slide_index'] = i + 1

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")
print("Bulk fixes applied!")
