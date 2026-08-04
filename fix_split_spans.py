import json
import re

with open('data/part01_data.js', 'r') as f:
    c = f.read()
start = c.find('[')
end = c.rfind(']')+1
data = json.loads(c[start:end])
theory = data[2]['theory']

# Let's find spans with 1 character or weird spaces
for s in theory:
    for t in s.get('text', []):
        if '🔊' in t:
            # Let's see how many speaker icons are in this slide's text
            count = t.count('🔊')
            if count > 2: # More than 2 means something is weird (should be max 2: one for word, one for phrase)
                print(f"Slide {s['slide_index']} has {count} speakers!")
                print(t)
