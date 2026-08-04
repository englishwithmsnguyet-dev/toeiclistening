import re

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Slide 9:
# <div style="color: #0284c7; font-weight: bold; font-size: 2rem; margin-bottom: 12px;">face /feɪs/</div>
def replace_s9(match):
    text = match.group(1)
    # clean text for JS string
    clean_t = text.replace('"', '&quot;').replace('`', '').strip()
    # The user wants to read the English word. "face /feɪs/" should probably just read "face".
    # But it's fine to let TTS read "face /feɪs/", TTS usually ignores phonetics or tries its best.
    # Actually let's just strip the phonetics.
    clean_t = clean_t.split('/')[0].strip()
    return f'<div style="color: #0284c7; font-weight: bold; font-size: 2rem; margin-bottom: 12px;">{text} <span onclick="playTTS(this.dataset.text, event)" data-text="{clean_t}" style="cursor: pointer; opacity: 0.5; font-size: 0.9em; margin-left: 4px;" onmouseover="this.style.opacity=\'1\'" onmouseout="this.style.opacity=\'0.5\'" title="Đọc từ này">🔊</span></div>'

content = re.sub(r'<div style="color: #0284c7; font-weight: bold; font-size: 2rem; margin-bottom: 12px;">(.*?)</div>', replace_s9, content)

# 2. Slide 11 & 17 and any others formatted by fix_dang2_edgecases:
# <div style="margin-bottom: 8px; font-weight: bold; color: #0284c7;">stand</div>
def replace_s11(match):
    text = match.group(1)
    # Don't add if already has 🔊
    if '🔊' in text:
        return match.group(0)
    clean_t = text.replace('"', '&quot;').replace('`', '').strip()
    clean_t = clean_t.split('/')[0].strip() # remove phonetic
    return f'<div style="margin-bottom: 8px; font-weight: bold; color: #0284c7;">{text} <span onclick="playTTS(this.dataset.text, event)" data-text="{clean_t}" style="cursor: pointer; opacity: 0.5; font-size: 0.9em; margin-left: 4px;" onmouseover="this.style.opacity=\'1\'" onmouseout="this.style.opacity=\'0.5\'" title="Đọc từ này">🔊</span></div>'

content = re.sub(r'<div style="margin-bottom: 8px; font-weight: bold; color: #0284c7;">(.*?)</div>', replace_s11, content)

with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected TTS specifically into Slide 9, 11, 17!")
