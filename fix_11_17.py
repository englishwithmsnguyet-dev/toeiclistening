with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

target_11 = '<div style="margin-bottom: 8px; font-weight: bold; color: #0284c7;">stand</div>'
rep_11 = '<div style="margin-bottom: 8px; font-weight: bold; color: #0284c7;">stand <span onclick="playTTS(this.dataset.text, event)" data-text="stand" style="cursor: pointer; opacity: 0.5; font-size: 0.9em; margin-left: 4px;" onmouseover="this.style.opacity=\'1\'" onmouseout="this.style.opacity=\'0.5\'" title="Đọc từ này">🔊</span></div>'

target_17 = '<div style="margin-bottom: 8px; font-weight: bold; color: #0284c7;">descend /dɪˈsend/</div>'
rep_17 = '<div style="margin-bottom: 8px; font-weight: bold; color: #0284c7;">descend /dɪˈsend/ <span onclick="playTTS(this.dataset.text, event)" data-text="descend" style="cursor: pointer; opacity: 0.5; font-size: 0.9em; margin-left: 4px;" onmouseover="this.style.opacity=\'1\'" onmouseout="this.style.opacity=\'0.5\'" title="Đọc từ này">🔊</span></div>'

content = content.replace(target_11, rep_11)
content = content.replace(target_17, rep_17)

with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Replaced exact strings for Slide 11 and 17!")
