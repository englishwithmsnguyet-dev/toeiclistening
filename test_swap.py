import re

html = '''<div style="display: flex; flex-direction: row; gap: 32px; justify-content: center; width: 100%; align-items: flex-start; margin-top: 10px;">
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/slide_53_img_6.jpg" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">pushing the luggage</strong></div><div style="margin-bottom: 8px;">đẩy hành lý</div>
    </div>
  </div>
  <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
    <img src="data/graphics/part01/slide_53_img_7.jpg" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
    <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
      <div style="margin-bottom: 8px;"><strong style="color: #00B050;">pushing the door</strong></div><div style="margin-bottom: 8px;">đẩy cánh cửa</div>
    </div>
  </div>
</div>'''

imgs = re.findall(r'src="([^"]+)"', html)
eng_texts = re.findall(r'<strong style="color: #00B050;">(.*?)</strong>', html)
viet_texts = []
for eng in eng_texts:
    pattern = r'<strong style="color: #00B050;">' + re.escape(eng) + r'</strong></div><div style="margin-bottom: 8px;">(.*?)</div>'
    m = re.search(pattern, html)
    if m:
        viet_texts.append(m.group(1))
    else:
        viet_texts.append("")
        
print("Images:", imgs)
print("Eng:", eng_texts)
print("Viet:", viet_texts)
