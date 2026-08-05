import json
import re

with open("data/part01_data.js", "r", encoding="utf-8") as f:
    content = f.read()

# Extract the JSON array
start_idx = content.find('[')
end_idx = content.rfind(']') + 1
json_str = content[start_idx:end_idx]
data = json.loads(json_str)

def clean_html(text):
    return re.sub(r'<[^>]+>', '', text)

# Find dang_02
for section in data:
    if section["id"] == "dang_02":
        for slide in section["theory"]:
            if 16 <= slide["slide_index"] <= 30: # Check all vocab slides
                if "text" in slide and len(slide["text"]) > 0:
                    html = slide["text"][0]
                    
                    # 1. Clean up TTS data-text attributes
                    def replace_data_text(match):
                        raw_text = match.group(1)
                        clean_text = clean_html(raw_text).replace('...', '').strip()
                        return f'data-text="{clean_text}"'
                    
                    html = re.sub(r'data-text="([^"]+)"', replace_data_text, html)
                    
                    # Store back temporarily
                    slide["text"][0] = html

# We will write the updated JSON back to part01_data.js
new_content = "window.part01Data = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n"
with open("data/part01_data.js", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Saved cleaned data-texts.")
