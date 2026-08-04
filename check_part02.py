import json

with open('data/part02_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('{')
end_idx = content.rfind('}') + 1
data = json.loads(content[start_idx:end_idx])

print("Part 2 slides count:", len(data['theory']))

# Look at the first few slides to understand their structure
for slide in data['theory'][:5]:
    print(f"--- Slide {slide.get('slide_index')} ---")
    if slide.get('images'):
        print("Images:", slide['images'])
    if slide.get('text'):
        print("Text preview:", slide['text'][0][:200])
