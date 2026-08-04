import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix Button styling
# Find: style="background: var(--primary); color: white;
content = content.replace(
    'style="background: var(--primary); color: white;',
    'style="background: #2563eb; color: white;'
)

# 2. Fix layout proportions and font-size
# Find: <div style="flex: 1; max-width: 45%; display: flex; justify-content: center; align-items: flex-start;">
content = content.replace(
    '<div style="flex: 1; max-width: 45%; display: flex; justify-content: center; align-items: flex-start;">',
    '<div style="flex: 1; max-width: 35%; display: flex; justify-content: center; align-items: flex-start;">'
)

# Find: <div style="flex: 1; min-width: 300px; max-width: 55%; font-size: 1.25rem;
content = content.replace(
    '<div style="flex: 1; min-width: 300px; max-width: 55%; font-size: 1.25rem;',
    '<div style="flex: 1; min-width: 300px; max-width: 65%; font-size: 1.15rem;'
)

# 3. Add text KIỂM TRA in uppercase and proper styling inside the button HTML?
# The button already has "Kiểm tra". The user says "chưa thấy chữ KIỂM TRA", which was due to white on white! But I'll make it uppercase "KIỂM TRA".
content = content.replace(
    '>Kiểm tra</button>',
    '>KIỂM TRA</button>'
)

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed layout in app.js!")
