import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('[')
end = content.rfind(']')+1
data = json.loads(content[start:end])
theory = data[2]['theory']

# Slide mapping in the CURRENT state (with Structure Slide added):
# Picture 2A = Slide 25
# Picture 2B = Slide 26
# Picture 01 = Slide 28
# Picture 02 = Slide 29
# Picture 03 = Slide 30
# Picture 04 = Slide 31
# Picture 05 = Slide 32
# Picture 06 = Slide 33

updates = {
    25: "D", # 2A (user's 24)
    26: "A", # 2B (user's 25)
    28: "A", # 01 (user's 27)
    30: "B"  # 03 (user's 29)
}

for s in theory:
    idx = s.get('slide_index')
    if idx in updates and s.get('practice'):
        print(f"Updating slide {idx} answer from {s['practice']['answer']} to {updates[idx]}")
        s['practice']['answer'] = updates[idx]

data[2]['theory'] = theory
out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")

print("Fixed answers!")
