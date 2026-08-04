import json

db_path = "/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/BÀI GIẢNG/toeic_listening_web/data/part04_data.json"
js_path = "/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/BÀI GIẢNG/toeic_listening_web/data/part04_data.js"

with open(db_path, "r", encoding="utf-8") as f:
    db = json.load(f)

for test_id in range(1, 6):
    test_key = f"test_{test_id:02d}"
    practice_sets = []
    
    q_start = 71
    for set_idx in range(1, 11):
        questions = []
        for q_offset in range(3):
            q_num = q_start + q_offset
            questions.append({
                "id": q_num,
                "slide_index": 3000 + q_num,
                "question": f"Question {q_num} (ETS 2026 Test {test_id} pending)",
                "choices": {
                    "A": "Option A",
                    "B": "Option B",
                    "C": "Option C",
                    "D": "Option D"
                },
                "answer": "A",
                "vietnamese_question": f"Câu hỏi {q_num} (Đang chờ cập nhật)",
                "vietnamese_choices": {
                    "A": "Lựa chọn A",
                    "B": "Lựa chọn B",
                    "C": "Lựa chọn C",
                    "D": "Lựa chọn D"
                },
                "explanation": f"<strong>ĐÁP ÁN ĐÚNG LÀ A</strong><br><em>(Dữ liệu bài thi đang được cập nhật)</em>"
            })
            
        practice_sets.append({
            "set_index": set_idx,
            "audio": f"E26-T{test_id:02d}-{q_start}-{q_start+2}.mp3",
            "questions": questions,
            "transcript": [f"(Pending transcript for questions {q_start}-{q_start+2})"],
            "vietnamese_transcript": [f"(Bản dịch đang được cập nhật)"]
        })
        q_start += 3

    for section in db:
        if section.get("id") == test_key:
            section["practice_sets"] = practice_sets
            break

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

with open(js_path, "w", encoding="utf-8") as f:
    f.write("window.part04Data = ")
    json.dump(db, f, ensure_ascii=False, indent=2)
    f.write(";\n")
print("Restored dummy data")
