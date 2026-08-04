import json

with open('data/part01_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('[')
end_idx = content.rfind(']') + 1
data = json.loads(content[start_idx:end_idx])

dang2 = data[2]['theory']

vocab_dict = {
    "2A": [
        {"en": "repair a motorcycle", "vi": "sửa xe máy"},
        {"en": "board a boat", "vi": "lên tàu"},
        {"en": "drive a car", "vi": "lái xe ô tô"},
        {"en": "walk along the water", "vi": "đi bộ dọc mép nước"}
    ],
    "2B": [
        {"en": "a waiting area", "vi": "khu vực chờ"},
        {"en": "place books", "vi": "đặt sách"},
        {"en": "move a chair", "vi": "di chuyển ghế"},
        {"en": "water a plant", "vi": "tưới cây"}
    ],
    "01": [
        {"en": "wear a scarf", "vi": "đeo khăn quàng cổ"},
        {"en": "talk to each other", "vi": "nói chuyện với nhau"},
        {"en": "pour coffee", "vi": "rót cà phê"},
        {"en": "close menus", "vi": "gấp thực đơn"}
    ],
    "02": [
        {"en": "hang a notice", "vi": "treo thông báo"},
        {"en": "a doorway", "vi": "lối ra vào"},
        {"en": "change a tire", "vi": "thay lốp xe"},
        {"en": "a cart", "vi": "xe đẩy"}
    ],
    "03": [
        {"en": "write on a notepad", "vi": "viết vào sổ tay"},
        {"en": "look at files", "vi": "nhìn vào tài liệu"},
        {"en": "sit at a desk", "vi": "ngồi ở bàn làm việc"},
        {"en": "face each other", "vi": "đối mặt nhau"}
    ],
    "04": [
        {"en": "travelers", "vi": "du khách"},
        {"en": "set up partition", "vi": "dựng vách ngăn"},
        {"en": "hand out tickets", "vi": "phát vé"},
        {"en": "approach a counter", "vi": "tiến đến quầy"}
    ],
    "05": [
        {"en": "sit in a car", "vi": "ngồi trong xe ô tô"},
        {"en": "face each other", "vi": "đối mặt nhau"},
        {"en": "open a handbag", "vi": "mở túi xách"},
        {"en": "remove a jacket", "vi": "cởi áo khoác"}
    ]
}

# Answers (guessed)
ans_dict = {
    "2A": "A",
    "2B": "B",
    "01": "B",
    "02": "B",
    "03": "D",
    "04": "A",
    "05": "B"
}

pic_idx = 0
keys = ["2A", "2B", "01", "02", "03", "04", "05"]

for slide in dang2:
    if slide.get('practice'):
        key = keys[pic_idx]
        slide['practice']['vocab'] = vocab_dict[key]
        slide['practice']['answer'] = ans_dict[key]
        pic_idx += 1

out_json = json.dumps(data, ensure_ascii=False, indent=2)
with open('data/part01_data.js', 'w', encoding='utf-8') as f:
    f.write(f"window.part01Data = {out_json};\n")
print("Injected vocabulary and answers for Dạng 2!")
