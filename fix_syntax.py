import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Practice Options
content = content.replace(
    'onclick="playTTS(`${opt.replace(/"/g, \'&quot;\')}`, event)"',
    'onclick="playTTS(this.dataset.text, event)" data-text="${opt.replace(/\"/g, \'&quot;\')}"'
)

# Fix Vocab
content = content.replace(
    'onclick="playTTS(`${v.en.replace(/"/g, \'&quot;\')}`, event)"',
    'onclick="playTTS(this.dataset.text, event)" data-text="${v.en.replace(/\"/g, \'&quot;\')}"'
)

# Fix playTTS signature to handle the new dataset approach
# Actually, the signature is window.playTTS = function(text, event)
# If it's called with `playTTS(this.dataset.text, event)`, it still receives text and event.

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content2 = f.read()

# Fix Theory Slides (which also used backticks!)
# onclick="playTTS(`{clean_t}`, event)" -> onclick="playTTS(this.dataset.text, event)" data-text="{clean_t}"
content2 = re.sub(
    r'onclick="playTTS\(\`([^`]+)\`,\s*event\)"',
    r'onclick="playTTS(this.dataset.text, event)" data-text="\1"',
    content2
)

with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(content2)

print("Syntax errors fixed!")
