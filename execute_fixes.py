import json
import re

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
json_str = content[start_idx:end_idx]

data = json.loads(json_str)

def swap_html_blocks(html):
    # Splits the HTML by finding the two columns and swapping their contents
    # The columns are <div> elements inside a flex container
    parts = re.split(r'(<div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">)', html)
    if len(parts) == 5:
        # parts[0] is the container opening
        # parts[1] is the delimiter
        # parts[2] is the first column content
        # parts[3] is the delimiter
        # parts[4] is the second column content and container closing
        
        # We just need to swap parts[2] and the content part of parts[4]
        # BUT parts[4] contains the closing </div></div> at the end.
        col2_content = parts[4].rsplit('</div>\n</div>', 1)[0]
        suffix = '</div>\n</div>' if '</div>\n</div>' in parts[4] else '</div></div>'
        
        # Or simpler, just swap the images and text blocks!
        # Actually, if we just swap the text strings inside the html? No, it's safer to swap the entire block.
        pass
    
    # A more robust way to swap left and right text (while keeping images in place)
    # The user said "lộn cụm" -> Swap the text, NOT the images. 
    # Or "không khớp ảnh" -> same thing, swap the text so it matches the image.
    # Let's extract the images and text separately and rebuild the HTML.
    imgs = re.findall(r'src="([^"]+)"', html)
    eng_texts = re.findall(r'<strong style="color: #00B050;">(.*?)</strong>', html)
    
    # Extract Viet texts
    # They are in the div following the eng_text div
    viet_texts = []
    for eng in eng_texts:
        # find <div style="margin-bottom: 8px;">{eng}</div><div style="margin-bottom: 8px;">{viet}</div>
        pattern = r'<strong style="color: #00B050;">' + re.escape(eng) + r'</strong></div><div style="margin-bottom: 8px;">(.*?)</div>'
        m = re.search(pattern, html)
        if m:
            viet_texts.append(m.group(1))
        else:
            viet_texts.append("")
            
    if len(imgs) == 2 and len(eng_texts) == 2 and len(viet_texts) == 2:
        return f'''<div style="display: flex; flex-direction: row; gap: 32px; justify-content: center; width: 100%; align-items: flex-start; margin-top: 10px;">
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="{imgs[0]}" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">{eng_texts[1]}</strong></div><div style="margin-bottom: 8px;">{viet_texts[1]}</div>
    </div>
  </div>
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="{imgs[1]}" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">{eng_texts[0]}</strong></div><div style="margin-bottom: 8px;">{viet_texts[0]}</div>
    </div>
  </div>
</div>'''
    return html

# 1. Extract Slide 37 (Grammar) from DẠNG 1
slide_37_obj = None
for s in data[0]['theory']:
    if s['slide_index'] == 37:
        slide_37_obj = s
        break
if slide_37_obj:
    data[0]['theory'].remove(slide_37_obj)
    # insert into DANG 2 right after title slide (slide_index 111)
    data[1]['theory'].insert(1, slide_37_obj)

# 2. Extract Slide 53 (tào lao) and delete
slide_53_obj = None
for s in data[0]['theory']:
    if s['slide_index'] == 53:
        slide_53_obj = s
        break
if slide_53_obj:
    data[0]['theory'].remove(slide_53_obj)

# Apply fixes to DẠNG 1
slides_to_swap = [43, 46, 52, 79, 82, 85, 88, 91, 94]

for slide in data[0]['theory']:
    idx = slide['slide_index']
    texts = slide.get('text', [])
    if not texts: continue
    html = texts[0]
    
    if idx == 20:
        html = html.replace('hanging a sign', 'hanging a sign on the wall')
        html = html.replace('treo một biển hiệu', 'treo biển hiệu trên tường')
        html = html.replace('hanging a jacket', 'hanging a jacket on a coat rack')
        html = html.replace('treo một chiếc áo khoác', 'treo áo khoác lên giá')
        slide['text'] = [html]
    elif idx == 26:
        html = html.replace('leaning against the wall', 'leaning against a car')
        html = html.replace('tựa vào bức tường', 'tựa vào chiếc xe hơi')
        slide['text'] = [html]
    elif idx == 40: # Broken HTML
        html = f'''<div style="display: flex; flex-direction: row; gap: 32px; justify-content: center; width: 100%; align-items: flex-start; margin-top: 10px;">
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/slide_50_img_6.jpg" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">pouring water into a cup</strong></div><div style="margin-bottom: 8px;">rót nước vào cốc</div>
    </div>
  </div>
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/slide_50_img_7.jpg" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">pouring liquid into a glass</strong></div><div style="margin-bottom: 8px;">rót chất lỏng vào ly</div>
    </div>
  </div>
</div>'''
        slide['text'] = [html]
    elif idx == 49: # Broken HTML
        html = f'''<div style="display: flex; flex-direction: row; gap: 32px; justify-content: center; width: 100%; align-items: flex-start; margin-top: 10px;">
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/slide_59_img_6.jpg" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">putting merchandise into a bag</strong></div><div style="margin-bottom: 8px;">bỏ hàng hoá vào túi</div>
    </div>
  </div>
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/slide_59_img_7.png" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">putting items in a backpack</strong></div><div style="margin-bottom: 8px;">bỏ đồ đạc vào ba lô</div>
    </div>
  </div>
</div>'''
        slide['text'] = [html]
    elif idx in slides_to_swap:
        slide['text'] = [swap_html_blocks(html)]
        
# Re-number DẠNG 1 theory sequentially
for i, slide in enumerate(data[0]['theory']):
    slide['slide_index'] = i + 1

# For Practice section, we need to clean up the layout.
# Let's inspect the practice section first to see what's wrong.
# We will just write the changes to data for now.
out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")

print("Fixed all theory issues. Now for Practice section...")
