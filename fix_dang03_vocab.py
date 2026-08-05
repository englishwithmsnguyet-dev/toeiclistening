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
            if not slide.get("text"):
                continue
            
            # Check if it has a vocabulary word (length 3, with the title)
            # Or if it has "CÁC GIỚI TỪ THƯỜNG GẶP" or "CÁC CỤM GIỚI TỪ THƯỜNG GẶP"
            first_line = slide["text"][0]
            if "CÁC GIỚI TỪ THƯỜNG GẶP" in first_line or "CÁC CỤM GIỚI TỪ THƯỜNG GẶP" in first_line:
                # Remove the title
                slide["text"].pop(0)
                
                # Now the first line is the English word, e.g. "<strong>in front of</strong>"
                if len(slide["text"]) > 0:
                    en_word_html = slide["text"][0]
                    # Extract raw text to pass to TTS
                    en_word_clean = re.sub(r'<[^>]+>', '', en_word_html).strip()
                    
                    # Wrap with the TTS button
                    # Keep the original HTML but add the TTS icon next to it
                    # Example: <div style="display: flex; align-items: center; justify-content: center; gap: 8px;"><strong>in front of</strong> <span onclick="playTTS('in front of', event)" ...>🔊</span></div>
                    
                    tts_icon = f'<span onclick="playTTS(\'{en_word_clean}\', event)" style="cursor: pointer; opacity: 0.7; font-size: 1.2rem; transition: opacity 0.2s;" onmouseover="this.style.opacity=\'1\'" onmouseout="this.style.opacity=\'0.7\'" title="Đọc từ này">🔊</span>'
                    
                    slide["text"][0] = f'<div style="display: flex; align-items: center; justify-content: center; gap: 12px; font-size: 1.2em;">{en_word_html} {tts_icon}</div>'
                
new_content = "window.part01Data = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n"
with open("data/part01_data.js", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Done fixing Dạng 03 vocabulary slides.")
