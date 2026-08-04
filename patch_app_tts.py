import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject playTTS function at the top (next to window.selectPracticeOption)
tts_func = """
window.playTTS = function(text, event) {
    if (event) event.stopPropagation(); // prevent triggering row click
    if (!('speechSynthesis' in window)) {
        alert("Trình duyệt của bạn không hỗ trợ tính năng đọc từ!");
        return;
    }
    
    // Stop any currently playing audio
    window.speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    
    // Try to find a good voice
    const voices = window.speechSynthesis.getVoices();
    let bestVoice = voices.find(v => v.lang === 'en-US' && v.name.includes('Google'));
    if (!bestVoice) bestVoice = voices.find(v => v.lang.startsWith('en-'));
    if (bestVoice) utterance.voice = bestVoice;
    
    // Adjust rate and pitch for clarity
    utterance.rate = 0.9;
    utterance.pitch = 1.0;
    
    window.speechSynthesis.speak(utterance);
};
"""

if "window.playTTS =" not in content:
    content = content.replace("window.selectPracticeOption = function(el) {", tts_func + "\nwindow.selectPracticeOption = function(el) {")

# 2. Update Practice Options rendering to include TTS button
# Find: <strong style="margin-right: 8px; font-size: 1.1em;">${labels[i]}.</strong> <span>${opt}</span>
# Replace with: <strong style="margin-right: 8px; font-size: 1.1em;">${labels[i]}.</strong> <span>${opt}</span> <span onclick="playTTS('${opt.replace(/'/g, "\\'")}', event)" style="cursor: pointer; margin-left: 8px; font-size: 1.2em; opacity: 0.6; transition: opacity 0.2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.6'" title="Nghe câu này">🔊</span>
content = content.replace(
    '<strong style="margin-right: 8px; font-size: 1.1em;">${labels[i]}.</strong> <span>${opt}</span>',
    '<strong style="margin-right: 8px; font-size: 1.1em;">${labels[i]}.</strong> <span>${opt}</span> <span class="tts-btn" onclick="playTTS(`${opt.replace(/"/g, \'&quot;\')}`, event)" style="cursor: pointer; margin-left: 8px; font-size: 1.2em; opacity: 0.5; transition: opacity 0.2s;" onmouseover="this.style.opacity=\'1\'" onmouseout="this.style.opacity=\'0.5\'" title="Nghe câu này">🔊</span>'
)

# 3. Update Vocab rendering to include TTS button
# Find: <span style="font-weight: 600; color: #0284c7; min-width: 140px; display: inline-block;">${v.en}</span>
# Replace with: <span style="font-weight: 600; color: #0284c7; min-width: 140px; display: inline-block;">${v.en} <span onclick="playTTS('${v.en.replace(/'/g, "\\'")}', event)" style="cursor: pointer; opacity: 0.5;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.5'">🔊</span></span>
content = content.replace(
    '<span style="font-weight: 600; color: #0284c7; min-width: 140px; display: inline-block;">${v.en}</span>',
    '<span style="font-weight: 600; color: #0284c7; min-width: 140px; display: inline-block;">${v.en} <span onclick="playTTS(`${v.en.replace(/"/g, \'&quot;\')}`, event)" style="cursor: pointer; margin-left: 4px; opacity: 0.5; font-size: 0.9em;" onmouseover="this.style.opacity=\'1\'" onmouseout="this.style.opacity=\'0.5\'" title="Đọc từ này">🔊</span></span>'
)

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated app.js with TTS logic!")
