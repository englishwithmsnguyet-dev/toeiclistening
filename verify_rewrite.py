import json
with open('data/part01_data.js', 'r') as f:
    c = f.read()
start = c.find('[')
end = c.rfind(']')+1
data = json.loads(c[start:end])
theory = data[2]['theory']

def dump(idx):
    s = theory[idx]
    print(f"\n--- Slide index {s.get('slide_index')} ---")
    print("Images:", s.get('images'))
    print("Audio:", s.get('audio'))
    if s.get('practice'):
        print("Practice audio:", s.get('practice', {}).get('audio'))
    for t in s.get('text', []):
        print(t)

for i, s in enumerate(theory):
    if s.get('slide_index') in [9, 11, 15, 17]:
        dump(i)
