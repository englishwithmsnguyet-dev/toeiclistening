import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

theory = data[1]['theory']

# Extract pay for (which has pay_left.png) and look (which has look_left_v2.png)
pay_slide = None
look_slide = None
bai_tap_slide = None

for slide in list(theory):
    if 'pay_left.png' in str(slide):
        pay_slide = slide
        theory.remove(slide)
    elif 'look_left_v2.png' in str(slide):
        look_slide = slide
        theory.remove(slide)

# Find the BÀI TẬP title slide
bai_tap_idx = -1
for i, slide in enumerate(theory):
    if 'BÀI TẬP' in str(slide['text']):
        bai_tap_idx = i
        break

if bai_tap_idx != -1:
    # Insert them before the BÀI TẬP slide
    if look_slide:
        theory.insert(bai_tap_idx, look_slide)
    if pay_slide:
        theory.insert(bai_tap_idx, pay_slide)
else:
    # If BÀI TẬP slide not found for some reason, just append to end
    if look_slide: theory.append(look_slide)
    if pay_slide: theory.append(pay_slide)

# Renumber all
for i, slide in enumerate(theory):
    slide['slide_index'] = i + 1

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")
print(f"Fixed slide order! New total slides: {len(theory)}")
