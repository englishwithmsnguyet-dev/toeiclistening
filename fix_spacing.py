import json
import re

with open("data/part01_data.js", "r", encoding="utf-8") as f:
    content = f.read()

start_idx = content.find("[")
end_idx = content.rfind("]") + 1
data = json.loads(content[start_idx:end_idx])

for section in data:
    if section["id"] == "dang_03":
        for slide in section.get("theory", []):
            if 30 <= slide.get("slide_index", 0) <= 35:
                # Add padding, margins, line heights
                for i in range(len(slide["text"])):
                    # Replace padding: 16px with padding: 24px
                    slide["text"][i] = slide["text"][i].replace("padding: 16px;", "padding: 24px;")
                    # Replace margin-bottom: 20px with margin-bottom: 32px
                    slide["text"][i] = slide["text"][i].replace("margin-bottom: 20px;", "margin-bottom: 32px;")
                    # Add line-height if not present
                    if "line-height" not in slide["text"][i]:
                        slide["text"][i] = slide["text"][i].replace('font-size: 1.2rem;', 'font-size: 1.2rem; line-height: 1.8;')
                        slide["text"][i] = slide["text"][i].replace('font-size: 1.4rem;', 'font-size: 1.4rem; line-height: 1.8;')
                        slide["text"][i] = slide["text"][i].replace('font-size: 1.1rem;', 'font-size: 1.1rem; line-height: 1.8;')
                        
new_content = "window.part01Data = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n"
with open("data/part01_data.js", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Spacing updated.")
