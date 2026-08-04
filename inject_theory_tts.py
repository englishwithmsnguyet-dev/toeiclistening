import re

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Target the format from format_dang2_fixed.py:
# <div style="margin-bottom: 8px; font-weight: bold; color: #0284c7;">{en1}</div>
# We want to add the speaker icon inside this div, and make it clickable.
# We need to capture the text {en1} to pass to playTTS.
def replace_div(match):
    text = match.group(1)
    # clean text for JS string
    clean_t = text.replace('"', '&quot;').replace('`', '').strip()
    return f'<div style="margin-bottom: 8px; font-weight: bold; color: #0284c7;">{text} <span onclick="playTTS(`{clean_t}`, event)" style="cursor: pointer; opacity: 0.5; font-size: 0.9em; margin-left: 4px;" onmouseover="this.style.opacity=\'1\'" onmouseout="this.style.opacity=\'0.5\'" title="Đọc từ này">🔊</span></div>'

content = re.sub(r'<div style="margin-bottom: 8px; font-weight: bold; color: #0284c7;">(.*?)</div>', replace_div, content)

# 2. What about Dang 1 theory slides?
# In Dang 1, I used a slightly different format (I didn't use fix_dang2_edgecases.py for Dang 1).
# I used format_part1_slides.py earlier (not in this exact session, but previously).
# Let's search for similar patterns in Dang 1. 
# They usually have: <div style="margin-bottom: 8px;">English Text</div>
# It might be harder to safely target Dang 1 without accidentally matching Vietnamese text.
# Let's just run this on the whole file, but only target the specific blue bold text which we know is English.

with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected TTS into theory slides!")
