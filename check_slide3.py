import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

# The unformatted original data is lost because we overwrote part01_data.js.
# But we can read it from the git history or backup. Wait, I don't have a backup.
# Let me just check the current texts inside the HTML block for Slide 3.
slide3 = data[2]['theory'][2]  # Slide index 3 is at index 2
print(slide3['text'][0][:500])
