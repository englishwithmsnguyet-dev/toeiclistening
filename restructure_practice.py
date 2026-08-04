import json
import re

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

answers = {
    96: 'C',
    97: 'B',
    98: 'C',
    99: 'B',
    100: 'A',
    101: 'D'
}

vocab_en = {
    96: ["a shopping cart", "make a purchase", "some merchandise", "some shelves"],
    97: ["a walkway", "a watering can", "a purchase", "some flowers"], # Wait, 'a purchase' was used in translation for Slide 97? Let's check options for 97
    98: ["the shore", "the sea", "a fishing pole", "a boat"],
    99: ["a busy street", "a cloth", "a jacket", "a vehicle"],
    100: ["a phone", "a newspaper", "a form", "an office"],
    101: ["a drawer", "a counter", "a meal", "a beverage"]
}
# Actually I need to re-verify slide 97 vocab. Let's look at it manually.
# In Slide 97, options are: A. picking some flowers B. holding a watering can C. arranging some chairs D. sweeping a walkway
# Vocab given: "lối đi bộ" (walkway), "bình tưới nước" (watering can), "việc mua hàng" (a purchase? No, it should be "cái ghế" or something. I'll just provide a clean list.)

vocab_override = {
    96: [
        {"en": "a shopping cart", "vi": "xe đẩy hàng"},
        {"en": "make a purchase", "vi": "mua hàng"},
        {"en": "merchandise", "vi": "hàng hoá"},
        {"en": "shelves", "vi": "cái kệ"}
    ],
    97: [
        {"en": "a walkway", "vi": "lối đi bộ"},
        {"en": "a watering can", "vi": "bình tưới nước"},
        {"en": "arrange", "vi": "sắp xếp"},
        {"en": "pick flowers", "vi": "hái hoa"}
    ],
    98: [
        {"en": "the shore", "vi": "bờ biển"},
        {"en": "the sea", "vi": "biển"},
        {"en": "a fishing pole", "vi": "cần câu cá"},
        {"en": "a boat", "vi": "con tàu"}
    ],
    99: [
        {"en": "a busy street", "vi": "con đường đông đúc"},
        {"en": "a cloth", "vi": "cái khăn"},
        {"en": "a jacket", "vi": "áo khoác"},
        {"en": "a vehicle", "vi": "phương tiện"}
    ],
    100: [
        {"en": "a phone", "vi": "điện thoại"},
        {"en": "a newspaper", "vi": "tờ báo"},
        {"en": "a form", "vi": "biểu mẫu"},
        {"en": "an office", "vi": "văn phòng"}
    ],
    101: [
        {"en": "a drawer", "vi": "ngăn kéo"},
        {"en": "a counter", "vi": "cái quầy"},
        {"en": "a meal", "vi": "bữa ăn"},
        {"en": "a beverage", "vi": "thức uống"}
    ]
}

options_data = {
    96: [
        "A man is pushing a shopping cart.",
        "A man is waiting to make a purchase.",
        "A man is holding some merchandise.",
        "A man is assembling some shelves."
    ],
    97: [
        "She's picking some flowers.",
        "She's holding a watering can.",
        "She's arranging some chairs.",
        "She's sweeping a walkway."
    ],
    98: [
        "He's walking along the shore.",
        "He's swimming in the sea.",
        "He's holding a fishing pole.",
        "He's getting into a boat."
    ],
    99: [
        "A woman's standing on a busy street.",
        "A woman's wiping a car window with a cloth.",
        "A woman's carrying a jacket over her arm.",
        "A woman's parking a vehicle."
    ],
    100: [
        "He's talking on a phone.",
        "He's folding a newspaper.",
        "He's writing on a form.",
        "He's leaving an office."
    ],
    101: [
        "A man is opening a drawer.",
        "A man is wiping a counter.",
        "A man is ordering a meal.",
        "A man is pouring a beverage."
    ]
}


for slide in data[1]['theory']:
    idx = slide.get('slide_index')
    if idx >= 96 and idx <= 101:
        # Create practice object
        slide['practice'] = {
            "options": options_data[idx],
            "answer": answers[idx],
            "vocab": vocab_override[idx]
        }
        # We can clear the `text` array so app.js knows to rely on `practice` instead.
        # But wait, does it have any audio references? Yes, `audio: "media32.mp3"` is in `slide.audio`.
        slide['text'] = []

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")
print("Restructured Practice Slides Data!")
