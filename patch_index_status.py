import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Part 3
html = html.replace('<span class="status-tag active">ĐÃ SẴN SÀNG</span>', '<span class="status-tag coming-soon">ĐÃ KHÓA</span>', 1)
# Part 2
html = html.replace('<span class="status-tag active">SLIDE SẴN SÀNG</span>', '<span class="status-tag coming-soon">ĐÃ KHÓA</span>', 1)
# Part 1 (Skip, it should remain active)
# Part 4
html = html.replace('<span class="status-tag active">ĐÃ SẴN SÀNG</span>', '<span class="status-tag coming-soon">ĐÃ KHÓA</span>', 1) # This replaces the second occurrence, which is Part 4

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html status tags!")
