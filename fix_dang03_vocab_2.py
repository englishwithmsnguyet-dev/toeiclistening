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
            
            first_line = slide["text"][0]
            if "CÁC CỤM TỪ VỊ TRÍ THƯỜNG GẶP" in first_line:
                # Remove the title
                slide["text"].pop(0)
                
                # The next line(s) might be the english words. 
                # Some slides have MULTIPLE english words, e.g. Slide 23 has:
                # '<strong>in a row</strong>'
                # '<strong>in a line</strong>'
                # '<span style="color: #0070C0;"><strong>TRONG MỘT HÀNG</strong></span>'
                
                # So we iterate and add TTS to every line that does not contain color #0070C0
                for i, line in enumerate(slide["text"]):
                    if "#0070C0" not in line and "trong một hàng" not in line.lower():
                        en_word_html = line
                        en_word_clean = re.sub(r'<[^>]+>', '', en_word_html).strip()
                        if en_word_clean:
                            # If it's not already wrapped
                            if "playTTS" not in line:
                                tts_icon = f'<span onclick="playTTS(\'{en_word_clean}\', event)" style="cursor: pointer; opacity: 0.7; font-size: 1.2rem; transition: opacity 0.2s;" onmouseover="this.style.opacity=\'1\'" onmouseout="this.style.opacity=\'0.7\'" title="Đọc từ này">🔊</span>'
                                slide["text"][i] = f'<div style="display: flex; align-items: center; justify-content: center; gap: 12px; font-size: 1.2em;">{en_word_html} {tts_icon}</div>'

new_content = "window.part01Data = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n"
with open("data/part01_data.js", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Done fixing Dạng 03 phrase slides.")
