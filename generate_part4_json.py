import re
import json
import urllib.request
import urllib.parse
import time
import os

CACHE_FILE = "translation_cache.json"

if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            translation_cache = json.load(f)
    except:
        translation_cache = {}
else:
    translation_cache = {}

def save_cache():
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(translation_cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        pass

def translate_text(text, target_lang="vi"):
    text = text.strip()
    if not text: return ""
    # Normalize spaces
    text = re.sub(r'\s+', ' ', text)
    
    cache_key = f"{target_lang}:{text}"
    if cache_key in translation_cache:
        return translation_cache[cache_key]
        
    for attempt in range(3):
        try:
            url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=" + target_lang + "&dt=t&q=" + urllib.parse.quote(text)
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode('utf-8'))
                translated = "".join([part[0] for part in result[0] if part[0]])
                translation_cache[cache_key] = translated
                save_cache()
                return translated
        except Exception as e:
            time.sleep(1)
    return text

def parse_questions():
    with open("raw_ocr_p4.txt", "r", encoding="utf-8") as f:
        content = f.read()
        
    # Clean up common OCR issues
    content = content.replace('\n\n', '\n')
    content = content.replace('(A}', '(A)').replace('{A)', '(A)').replace('[A]', '(A)')
    content = content.replace('(B}', '(B)').replace('{B)', '(B)').replace('[B]', '(B)')
    content = content.replace('(C}', '(C)').replace('{C)', '(C)').replace('[C]', '(C)')
    content = content.replace('(D}', '(D)').replace('{D)', '(D)').replace('[D]', '(D)')

    # Find all question blocks. Number from 71 to 100.
    # regex matches: " 71. What is... \n (A) ... \n (B) ... \n (C) ... \n (D) ... "
    pattern = r'(?m)^([789]\d|100)\.\s+(.*?)(?=\n\s*\([A-D]\)|\n\s*\d{2}\.|\Z)'
    
    questions = []
    
    # We will split the content by lines, it's easier to parse sequentially
    lines = content.split('\n')
    current_q = None
    
    q_pattern = re.compile(r'^([789]\d|100)[\.\,]\s*(.*)$')
    opt_pattern = re.compile(r'\(([A-D])\)\s*(.*)$')
    
    for i in range(len(lines)):
        line = lines[i].strip()
        if not line: continue
        
        # Sometimes options are on the same line: "(A) ... (B) ... (C) ... (D) ..."
        # We handle single line options if needed, but let's assume they are separated or we can separate them
        
        # Quick fix for multiple options on one line
        line = re.sub(r'(\([A-D]\))', r'\n\1', line).strip()
        sub_lines = [s.strip() for s in line.split('\n') if s.strip()]
        
        for s_line in sub_lines:
            q_match = q_pattern.match(s_line)
            if q_match:
                if current_q and len(current_q['choices']) >= 2:
                    questions.append(current_q)
                    
                q_num = int(q_match.group(1))
                q_text = q_match.group(2).strip()
                current_q = {
                    'id': q_num,
                    'question': q_text,
                    'choices': {}
                }
                continue
                
            opt_match = opt_pattern.match(s_line)
            if opt_match and current_q:
                opt_letter = opt_match.group(1)
                opt_text = opt_match.group(2).strip()
                current_q['choices'][opt_letter] = opt_text
                continue
                
            if current_q and len(current_q['choices']) == 0:
                # Continuation of question text
                current_q['question'] += " " + s_line
            elif current_q and len(current_q['choices']) > 0:
                # Continuation of option text (usually the last added option)
                last_opt = list(current_q['choices'].keys())[-1]
                current_q['choices'][last_opt] += " " + s_line

    if current_q and len(current_q['choices']) >= 2:
        questions.append(current_q)
        
    return questions

def generate_json(questions):
    # Questions array contains all parsed questions sequentially.
    # A new test starts when question ID drops (e.g. 100 -> 71) or is 71.
    
    tests = []
    current_test = []
    
    for q in questions:
        if q['id'] == 71 and len(current_test) > 0:
            tests.append(current_test)
            current_test = []
        current_test.append(q)
    if len(current_test) > 0:
        tests.append(current_test)
        
    print(f"Found {len(tests)} tests.")
    for idx, t in enumerate(tests):
        print(f"Test {idx+1}: {len(t)} questions")
    
    # Load base json structure
    db_path = "/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/BÀI GIẢNG/toeic_listening_web/data/part04_data.json"
    with open(db_path, "r", encoding="utf-8") as f:
        db = json.load(f)
        
    for test_idx, t_questions in enumerate(tests[:5]): # max 5 tests
        test_id = test_idx + 1
        test_key = f"test_{test_id:02d}"
        
        practice_sets = []
        
        # Group by 3 questions
        q_groups = [t_questions[i:i+3] for i in range(0, len(t_questions), 3)]
        
        for set_idx, group in enumerate(q_groups):
            if not group: continue
            
            q_start = group[0]['id']
            q_end = group[-1]['id']
            
            formatted_questions = []
            for q in group:
                print(f"Translating T{test_id} Q{q['id']}...")
                vi_q = translate_text(q['question'])
                vi_choices = {}
                for k, v in q['choices'].items():
                    vi_choices[k] = translate_text(v)
                    
                formatted_questions.append({
                    "id": q['id'],
                    "slide_index": 3000 + q['id'],
                    "question": q['question'],
                    "choices": q['choices'],
                    "answer": "A", # default
                    "vietnamese_question": f"Câu hỏi {q['id']}: {vi_q}",
                    "vietnamese_choices": vi_choices,
                    "explanation": f"<strong>ĐÁP ÁN ĐÚNG LÀ A</strong><br><em>(Dữ liệu bài thi đang được cập nhật)</em>"
                })
                
            practice_sets.append({
                "set_index": set_idx + 1,
                "audio": f"E26-T{test_id:02d}-{q_start}-{q_end}.mp3",
                "questions": formatted_questions,
                "transcript": [f"(Pending transcript for questions {q_start}-{q_end})"],
                "vietnamese_transcript": [f"(Bản dịch đang được cập nhật)"]
            })
            
        # Update db
        for section in db:
            if section.get("id") == test_key:
                section["practice_sets"] = practice_sets
                break
                
    # Save json
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    # Save js
    js_path = "/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/BÀI GIẢNG/toeic_listening_web/data/part04_data.js"
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("window.part04Data = ")
        json.dump(db, f, ensure_ascii=False, indent=2)
        f.write(";\n")
        
    print("Done!")

if __name__ == "__main__":
    qs = parse_questions()
    generate_json(qs)
