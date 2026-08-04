import json
import re

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
json_str = content[start_idx:end_idx]

data = json.loads(json_str)

md = "# Visual Audit of Multiple-Image Slides\n\n"
md += "Please review these slides to see if the texts match the images. Let me know which slides have mismatched text/images.\n\n"

for section in data:
    if 'theory' in section:
        for slide in section['theory']:
            idx = slide['slide_index']
            if idx > 111: break
            
            texts = slide.get('text', [])
            if not texts: continue
            
            html = texts[0]
            if 'display: flex' in html:
                imgs = re.findall(r'src="([^"]+)"', html)
                
                # Extract all text, strip HTML
                clean_text = re.sub(r'<[^>]+>', ' ', html)
                clean_text = ' '.join(clean_text.split())
                
                md += f"## Slide {idx}\n"
                md += f"**Text on Slide:** {clean_text}\n\n"
                
                md += "| Image 1 | Image 2 |\n"
                md += "|---|---|\n"
                
                row = []
                for img in imgs:
                    img_name = img.split('/')[-1]
                    abs_path = f"/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/BÀI GIẢNG/toeic_listening_web/data/graphics/part01/{img_name}"
                    row.append(f"![{img_name}](file://{abs_path})")
                
                if len(row) == 2:
                    md += f"| {row[0]} | {row[1]} |\n\n"
                else:
                    md += f"Images: {imgs}\n\n"
                    
                md += "---\n\n"

with open('/Users/nguyetpham/.gemini/antigravity/brain/915962ce-dd45-403f-9aab-7380a34b0eab/audit_images.md', 'w', encoding='utf-8') as f:
    f.write(md)
