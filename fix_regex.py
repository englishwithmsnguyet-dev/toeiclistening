import re

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

def swap_html(html_str):
    # This function swaps the image SRCs instead of the texts
    # This guarantees the text stays where it is, but the images swap sides
    imgs = re.findall(r'src=\\"([^"]+)\\"', html_str)
    if len(imgs) == 2:
        new_html = html_str.replace(imgs[0], 'TEMP_IMG')
        new_html = new_html.replace(imgs[1], imgs[0])
        new_html = new_html.replace('TEMP_IMG', imgs[1])
        return new_html
    return html_str

# Manually list the exact strings we want to swap images for
targets = [
    # Slide 43
    'pushing the luggage', 
    # Slide 46
    'pulling a cart', 
    # Slide 52
    'reaching into a bag', 
    # Slide 79
    'wearing a long-sleeved shirt', 
    # Slide 82
    'putting on gloves', 
    # Slide 85
    'working in an office', 
    # Slide 88
    'writing on a notebook', 
    # Slide 91
    'folding a towel', 
    # Slide 94
    'wiping a window'
]

# We need to find the full <div> block that contains these targets.
# The block starts with "<div style=\"display: flex;" and ends with "</div>\n</div>\""
blocks = re.findall(r'(\\"<div style=\\"display: flex;.*?</div></div>\\")', content, flags=re.DOTALL)
if not blocks:
    # try another ending
    blocks = re.findall(r'(\\"<div style=\\"display: flex;.*?</div>\\n</div>\\")', content, flags=re.DOTALL)

for target in targets:
    for block in blocks:
        if target in block:
            new_block = swap_html(block)
            content = content.replace(block, new_block)
            print(f"Swapped images for block containing: {target}")
            break

with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(content)
