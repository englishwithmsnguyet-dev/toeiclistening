import json

with open('data/part01_data.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

print("--- Check Slide 8 and 9 images ---")
print("Slide 8 images:", old_data[2]['theory'][7].get('images'))
print("Slide 8 text:", [t[:50] for t in old_data[2]['theory'][7].get('text', [])])
print("Slide 9 images:", old_data[2]['theory'][8].get('images'))

print("\n--- Check Slide 15 audio ---")
# Index 14 in dang2_raw?
print("Index 14 audio:", old_data[2]['theory'][14].get('audio'))
print("Index 14 text:", [t[:50] for t in old_data[2]['theory'][14].get('text', [])])

print("\n--- Check Slide 11 images ---")
print("Slide 11 images:", old_data[2]['theory'][10].get('images'))

print("\n--- Check Slide 17 images ---")
print("Slide 17 images:", old_data[2]['theory'][16].get('images'))
