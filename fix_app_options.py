with open('js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

target = '<strong style="margin-right: 8px; font-size: 1.1em;">${labels[i]}.</strong> <span>${opt}</span> <span class="tts-btn" onclick="playTTS(this.dataset.text, event)" data-text="${opt.replace(/\"/g, \'&quot;\')}" style="cursor: pointer; margin-left: 8px; font-size: 1.2em; opacity: 0.5; transition: opacity 0.2s;" onmouseover="this.style.opacity=\'1\'" onmouseout="this.style.opacity=\'0.5\'" title="Nghe câu này">🔊</span>'
replacement = '<strong style="margin-right: 8px; font-size: 1.1em;">${labels[i]}.</strong> <span>${opt}</span>'

content = content.replace(target, replacement)

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed exactly!")
