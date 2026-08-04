import json
import re

with open('data/part01_data.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()
start_idx = content.find('[')
end_idx = content.rfind(']') + 1
current_data = json.loads(content[start_idx:end_idx])

dang2_raw = old_data[2]['theory']
new_theory = []

def clean_text(t):
    return re.sub(r'<[^>]+>', '', t).replace('`', '').strip()

def get_first_text(slide):
    texts = slide.get('text', [])
    return texts[0] if len(texts) > 0 else ""

def inject_tts(text_html):
    def repl(m):
        full_span = m.group(0)
        word = m.group(1).replace('"', '&quot;').replace('`', '').strip()
        tts_btn = f' <span onclick="playTTS(this.dataset.text, event)" data-text="{word}" style="cursor: pointer; opacity: 0.5; font-size: 0.9em; margin-left: 4px; display: inline-block;" onmouseover="this.style.opacity=\'1\'" onmouseout="this.style.opacity=\'0.5\'" title="Đọc từ này">🔊</span>'
        return full_span + tts_btn
    return re.sub(r'<span style="color: #0070C0;"><strong>(.*?)</strong></span>', repl, text_html)

def format_text_block(texts):
    res = ""
    for t in texts:
        t_injected = inject_tts(t)
        res += f'<div style="margin-bottom: 12px; font-size: 1.3rem;">{t_injected}</div>'
    return res

i = 0
while i < len(dang2_raw):
    slide = dang2_raw[i].copy()
    texts = slide.get('text', [])
    first_text = texts[0] if len(texts) > 0 else ""
    imgs = slide.get('images', [])
    
    # 1. Skip CẤU TRÚC CHÍNH
    if 'CẤU TRÚC' in first_text or 'CẤU TRÚC' in clean_text(first_text).upper():
        i += 1
        continue
        
    # 2. Title slide
    if 'TRANH CÓ NHIỀU NGƯỜI' in first_text:
        new_theory.append(slide)
        i += 1
        continue

    # 3. PRACTICE Title Slide (Slide 26)
    if 'PRACTICE' in first_text:
        if len(imgs) == 6:
            img_html = "".join([f'<img src="data/graphics/part01/{img}" style="width: 30%; max-height: 150px; object-fit: contain; margin: 10px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">' for img in imgs])
            html = f'<div style="text-align: center; margin-bottom: 24px; font-size: 2rem; color: #dc2626; font-weight: bold;">{clean_text(first_text)}</div><div style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center; width: 100%; max-width: 900px; margin: 0 auto;">{img_html}</div>'
            slide['text'] = [html]
            slide['images'] = []
        new_theory.append(slide)
        i += 1
        continue

    # 4. Theory Slides (2 images)
    if len(imgs) == 2:
        title = inject_tts(texts[0]) if len(texts) > 0 else ""
        left_texts, right_texts = [], []
        
        if len(texts) == 10 and 'stand' in clean_text(texts[2]):
            left_texts = [texts[2], texts[3], texts[6], texts[8]]
            right_texts = [texts[4], texts[5], texts[7], texts[9]]
        elif len(texts) == 4 and 'descend' in clean_text(texts[1]):
            left_texts = [texts[1], texts[2], texts[3]]
            right_texts = [texts[1], texts[2], texts[3]]
        elif len(texts) == 5:
            en1 = texts[1]
            en2 = texts[2]
            vi1 = texts[3]
            vi2 = texts[4]
            if 'the people' in clean_text(en1).lower() and 'one of' in clean_text(en2).lower():
                vi1, vi2 = vi2, vi1
            left_texts = [en1, vi1]
            right_texts = [en2, vi2]
        else:
            half = len(texts) // 2
            left_texts = texts[1:half+1]
            right_texts = texts[half+1:]
            
        html = f"""<div style="text-align: center; margin-bottom: 24px; font-size: 1.5rem;">{title}</div>
<div style="display: flex; flex-direction: row; gap: 32px; justify-content: center; width: 100%; align-items: flex-start;">
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center;">
    <img src="data/graphics/part01/{imgs[0]}" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="color: var(--text-main); text-align: center;">{format_text_block(left_texts)}</div>
  </div>
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center;">
    <img src="data/graphics/part01/{imgs[1]}" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="color: var(--text-main); text-align: center;">{format_text_block(right_texts)}</div>
  </div>
</div>"""
        slide['text'] = [html]
        slide['images'] = []
        new_theory.append(slide)
        i += 1
        continue

    # 5. Missing Image Verb Slide (Slide 9 - face)
    if len(imgs) == 0 and len(texts) == 5 and 'CÁC ĐỘNG TỪ' in first_text:
        title = inject_tts(texts[0])
        body_texts = texts[1:]
        html = f"""<div style="text-align: center; margin-bottom: 24px; font-size: 1.5rem;">{title}</div>
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; margin-top: 40px; color: var(--text-main);">
  {format_text_block(body_texts)}
</div>"""
        slide['text'] = [html]
        new_theory.append(slide)
        i += 1
        continue

    # 6. Single-slide practice (Picture 2A, 2B)
    if 'PICTURE' in first_text and len(imgs) == 1:
        options_raw = texts[1:5]
        options = [clean_text(opt)[3:] for opt in options_raw] 
        slide['practice'] = {
            "options": options,
            "answer": "A",
            "vocab": [{"en": "vocab 1", "vi": "nghĩa 1"}]
        }
        slide['text'] = []
        new_theory.append(slide)
        i += 1
        continue
        
    # 7. Split-slide practice (Image slide + Text slide)
    if len(imgs) == 1 and len(texts) == 0:
        if i + 1 < len(dang2_raw) and 'PICTURE' in get_first_text(dang2_raw[i+1]):
            next_slide = dang2_raw[i+1]
            options_raw = next_slide['text'][1:5]
            options = [clean_text(opt)[3:] for opt in options_raw if opt != '`']
            
            slide['practice'] = {
                "options": options,
                "answer": "A",
                "vocab": [{"en": "vocab 1", "vi": "nghĩa 1"}]
            }
            slide['text'] = []
            new_theory.append(slide)
            i += 2
            continue
            
    # 8. Other theory slides (1 image)
    if 'PICTURE' not in first_text and 'PRACTICE' not in first_text:
        if len(imgs) == 1 and len(texts) > 0:
            title = inject_tts(texts[0]) if len(texts) > 0 else ""
            body_texts = texts[1:] if len(texts) > 1 else []
            html = f"""<div style="text-align: center; margin-bottom: 24px; font-size: 1.5rem;">{title}</div>
<div style="display: flex; flex-direction: row; gap: 32px; align-items: center; justify-content: center; width: 100%;">
  <div style="flex: 1; max-width: 50%;">
    <img src="data/graphics/part01/{imgs[0]}" style="width: 100%; max-height: 350px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08);">
  </div>
  <div style="flex: 1; color: var(--text-main);">
    {format_text_block(body_texts)}
  </div>
</div>"""
            slide['text'] = [html]
            slide['images'] = []
            new_theory.append(slide)
            i += 1
            continue

    # Fallback
    slide['text'] = [inject_tts(t) for t in slide.get('text', [])]
    new_theory.append(slide)
    i += 1

# Renumber
for idx, slide in enumerate(new_theory):
    slide['slide_index'] = idx + 1

vocab_dict = {
    "2A": [{"en": "repair a motorcycle", "vi": "sửa xe máy"}, {"en": "board a boat", "vi": "lên tàu"}, {"en": "drive a car", "vi": "lái xe ô tô"}, {"en": "walk along the water", "vi": "đi bộ dọc mép nước"}],
    "2B": [{"en": "a waiting area", "vi": "khu vực chờ"}, {"en": "place books", "vi": "đặt sách"}, {"en": "move a chair", "vi": "di chuyển ghế"}, {"en": "water a plant", "vi": "tưới cây"}],
    "01": [{"en": "wear a scarf", "vi": "đeo khăn quàng cổ"}, {"en": "talk to each other", "vi": "nói chuyện với nhau"}, {"en": "pour coffee", "vi": "rót cà phê"}, {"en": "close menus", "vi": "gấp thực đơn"}],
    "02": [{"en": "hang a notice", "vi": "treo thông báo"}, {"en": "a doorway", "vi": "lối ra vào"}, {"en": "change a tire", "vi": "thay lốp xe"}, {"en": "a cart", "vi": "xe đẩy"}],
    "03": [{"en": "write on a notepad", "vi": "viết vào sổ tay"}, {"en": "look at files", "vi": "nhìn vào tài liệu"}, {"en": "sit at a desk", "vi": "ngồi ở bàn làm việc"}, {"en": "face each other", "vi": "đối mặt nhau"}],
    "04": [{"en": "travelers", "vi": "du khách"}, {"en": "set up partition", "vi": "dựng vách ngăn"}, {"en": "hand out tickets", "vi": "phát vé"}, {"en": "approach a counter", "vi": "tiến đến quầy"}],
    "05": [{"en": "sit in a car", "vi": "ngồi trong xe ô tô"}, {"en": "face each other", "vi": "đối mặt nhau"}, {"en": "open a handbag", "vi": "mở túi xách"}, {"en": "remove a jacket", "vi": "cởi áo khoác"}],
    "06": [{"en": "look into a copy machine", "vi": "nhìn vào máy photo"}, {"en": "post notices on a board", "vi": "dán thông báo lên bảng"}, {"en": "put papers in a file", "vi": "đặt tài liệu vào tệp"}, {"en": "move equipment", "vi": "di chuyển thiết bị"}]
}
ans_dict = {"2A": "A", "2B": "B", "01": "B", "02": "B", "03": "D", "04": "A", "05": "B", "06": "A"}
keys = ["2A", "2B", "01", "02", "03", "04", "05", "06"]
pic_idx = 0

for slide in new_theory:
    if slide.get('practice'):
        key = keys[pic_idx]
        slide['practice']['vocab'] = vocab_dict[key]
        slide['practice']['answer'] = ans_dict[key]
        pic_idx += 1

current_data[2]['theory'] = new_theory
out_json = json.dumps(current_data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")
print("PERFECTLY FORMATTED DẠNG 2 CONTENT WITH TTS!")
