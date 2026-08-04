import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace all occurrences of "portal_unlocked" with "portal_unlocked_v2"
js = js.replace('"portal_unlocked"', '"portal_unlocked_v2"')

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated session storage key!")
