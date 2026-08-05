import json
import re

with open("data/part01_data.js", "r", encoding="utf-8") as f:
    content = f.read()

start_idx = content.find("[")
end_idx = content.rfind("]") + 1
data = json.loads(content[start_idx:end_idx])

for section in data:
    if section["id"] == "dang_02":
        for slide in section.get("theory", []):
            if not slide.get("text"): continue
            
            # Use regex to find and replace data-text="..."
            # where the text might contain HTML tags or phonetics.
            # Example: data-text="chat </strong>/</strong>tʃæt</strong>/"
            
            html = slide["text"][0]
            
            def clean_data_text(match):
                raw = match.group(1)
                # Remove html tags
                raw = re.sub(r'<[^>]+>', '', raw)
                # Remove phonetics: anything between slashes, or starting from a slash
                # e.g., "chat /tʃæt/" -> "chat"
                raw = re.sub(r'/.*?/', '', raw)
                raw = raw.replace('/', '').strip()
                return f'data-text="{raw}"'
            
            new_html = re.sub(r'data-text="(.*?)"', clean_data_text, html)
            slide["text"][0] = new_html

new_content = "window.part01Data = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n"
with open("data/part01_data.js", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Done fixing dang_02 TTS data-text.")
