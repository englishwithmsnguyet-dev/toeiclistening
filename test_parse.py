import json

with open("data/part01_data.js", "r", encoding="utf-8") as f:
    content = f.read()

start_idx = content.find("[")
end_idx = content.rfind("]") + 1
data = json.loads(content[start_idx:end_idx])

# Now check dang_01 (Wait, is it topic_01? No, Dạng 01 and 02 are dang_01 and dang_02)
# Oh, dang_01 is for Part 1 Dạng 1! Let's check IDs.
for section in data:
    if section["id"] in ["dang_01", "dang_02", "topic_01"]:
        print(f"Found section {section['id']}")
        for slide in section.get("theory", []):
            text_concat = " ".join(slide.get("text", []))
            if "BÀI TẬP" in text_concat.upper() or "(A)" in text_concat:
                print(f"  Slide {slide.get('slide_index')} has practice format:")
                print(json.dumps(slide["text"][:2], indent=2, ensure_ascii=False))
                break
