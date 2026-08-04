with open('js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to make playTTS strip HTML tags just in case
old_playTTS = """window.playTTS = function(text, event) {
    if (event) {
        event.stopPropagation();
    }
    if (!text) return;"""

new_playTTS = """window.playTTS = function(text, event) {
    if (event) {
        event.stopPropagation();
    }
    if (!text) return;
    
    // Strip any HTML tags that might have leaked into data-text
    text = text.replace(/<[^>]*>?/gm, '');"""

content = content.replace(old_playTTS, new_playTTS)

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched playTTS to strip HTML!")
