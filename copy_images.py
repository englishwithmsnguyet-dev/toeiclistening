import shutil
import os

uploads = '/Users/nguyetpham/.gemini/antigravity/brain/915962ce-dd45-403f-9aab-7380a34b0eab/.user_uploaded/'
dest = 'data/graphics/part01/'

mapping = {
    'media__1785465809720.png': 'slide_30_img_hold.png',
    'media__1785465841341.png': 'slide_33_img_lean.png',
    'media__1785465896074.png': 'slide_35_img_6_new.png',
    'media__1785465938537.png': 'slide_39_img_look.png',
    'media__1785466016137.png': 'slide_62_img_7.png'
}

for src, dst in mapping.items():
    src_path = os.path.join(uploads, src)
    dst_path = os.path.join(dest, dst)
    shutil.copy2(src_path, dst_path)
    print(f"Copied {src} to {dst}")
