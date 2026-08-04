import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start_idx = js.find('function loadSection(')
if start_idx != -1:
    end_idx = js.find('function ', start_idx + 10)
    print("loadSection:")
    print(js[start_idx:start_idx+300])

print("---")

start_idx2 = js.find('function loadSectionP4(')
if start_idx2 != -1:
    end_idx2 = js.find('function ', start_idx2 + 10)
    print("loadSectionP4:")
    print(js[start_idx2:start_idx2+300])
