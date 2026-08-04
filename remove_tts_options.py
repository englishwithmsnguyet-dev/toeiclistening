import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove TTS from practice options
# Current format: 
# <strong style="margin-right: 8px; font-size: 1.1em;">${labels[i]}.</strong> <span>${opt}</span> <span class="tts-btn" onclick="playTTS(this.dataset.text, event)" data-text="${opt.replace(/\"/g, '&quot;')}" style="cursor: pointer; margin-left: 8px; font-size: 1.2em; opacity: 0.5; transition: opacity 0.2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.5'" title="Nghe câu này">🔊</span>
# We just want to revert to:
# <strong style="margin-right: 8px; font-size: 1.1em;">${labels[i]}.</strong> <span>${opt}</span>

content = re.sub(
    r'<strong style="margin-right: 8px; font-size: 1.1em;">\$\{labels\[i\]\}\.</strong> <span>\$\{opt\}</span>\s*<span class="tts-btn" onclick="playTTS\(this\.dataset\.text, event\)" data-text="\$\{opt\.replace\(/\\"/g, \'&quot;\'\)\}" style="[^"]*" onmouseover="[^"]*" onmouseout="[^"]*" title="[^"]*">🔊</span>',
    r'<strong style="margin-right: 8px; font-size: 1.1em;">${labels[i]}.</strong> <span>${opt}</span>',
    content
)

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed TTS from options!")
