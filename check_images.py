import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
json_str = content[start_idx:end_idx]

data = json.loads(json_str)

issues = []

for section in data:
    if 'theory' in section:
        for slide in section['theory']:
            idx = slide['slide_index']
            if idx > 110:
                continue
            
            imgs = slide.get('images', [])
            texts = slide.get('text', [])
            text_preview = texts[0][:50] if texts else ''
            
            # Look for slides with 0 images, but text doesn't look like a title or it's just plain text
            if len(imgs) == 0:
                # Unless it's a slide we reformatted to put images in HTML
                # Let's check if there is an <img tag in the text
                has_img_in_html = any('<img' in t for t in texts)
                
                if not has_img_in_html and not "CẤU TRÚC" in text_preview and not "DẠNG" in text_preview and not "LƯU Ý" in text_preview and "BÀI TẬP" not in text_preview and "Subject" not in text_preview:
                    issues.append(f"Slide {idx}: No images found! Text: {text_preview}")
                    
print("Potential Missing Images:")
for issue in issues:
    print(issue)
