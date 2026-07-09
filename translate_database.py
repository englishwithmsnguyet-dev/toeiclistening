import json
import urllib.request
import urllib.parse
import time
import os
import re

CACHE_FILE = "translation_cache.json"
DATA_FILE = "data/part03_data.json"
OUTPUT_FILE = "data/part03_data.json"
JS_OUTPUT_FILE = "data/part03_data.js"

# Load translation cache
if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            translation_cache = json.load(f)
    except:
        translation_cache = {}
else:
    translation_cache = {}

def save_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(translation_cache, f, ensure_ascii=False, indent=2)

def translate_text(text, target_lang='vi'):
    text = text.strip()
    if not text:
        return ""
    
    # Check cache
    cache_key = f"{target_lang}:{text}"
    if cache_key in translation_cache:
        return translation_cache[cache_key]
    
    # Handle HTML tags or speaker labels
    # If there is a speaker prefix like "M: " or "W: " or "M-Cn: " or "W-Br: "
    prefix = ""
    prefix_match = re.match(r'^([A-Za-z]+[-A-Za-z]*\s*:\s*)(.*)', text, re.DOTALL)
    if prefix_match:
        prefix = prefix_match.group(1)
        text_to_translate = prefix_match.group(2)
    else:
        text_to_translate = text

    # Remove html tags for clean translation, then restore or just translate plain text
    clean_text = re.sub(r'<[^>]+>', '', text_to_translate).strip()
    if not clean_text:
        return text

    # Google single single-translate API
    for attempt in range(3):
        try:
            url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=" + target_lang + "&dt=t&q=" + urllib.parse.quote(clean_text)
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode('utf-8'))
                translated = "".join([part[0] for part in result[0] if part[0]])
                
                # Cache and return
                final_val = prefix + translated
                translation_cache[cache_key] = final_val
                save_cache()
                return final_val
        except Exception as e:
            print(f"Attempt {attempt+1} failed for: '{clean_text[:30]}...'. Error: {e}")
            time.sleep(1)
            
    # Return original text on failure
    return text

def generate_explanation(q_text, choices, answer, transcript, vietnamese_choices, vietnamese_transcript):
    # Auto-generate a beautiful Vietnamese explanation
    correct_choice_text = choices.get(answer, "")
    translated_choice_text = vietnamese_choices.get(answer, "")
    
    # Try to find the sentence in the transcript that matches the correct answer keywords
    best_matching_sentence = ""
    best_matching_viet_sentence = ""
    
    keywords = [w.lower() for w in re.findall(r'\b\w{4,}\b', correct_choice_text) if w.lower() not in ['what', 'when', 'where', 'with', 'they', 'their', 'some', 'from', 'this', 'that']]
    
    if transcript and len(transcript) > 0:
        for idx, line in enumerate(transcript):
            # Clean speaker label
            line_clean = re.sub(r'^[A-Za-z]+[-A-Za-z]*\s*:\s*', '', line).strip()
            line_lower = line_clean.lower()
            
            # Check if any keyword fits
            match_score = sum(1 for kw in keywords if kw in line_lower)
            if match_score > 0:
                best_matching_sentence = line_clean
                if idx < len(vietnamese_transcript):
                    best_matching_viet_sentence = re.sub(r'^[A-Za-z]+[-A-Za-z]*\s*:\s*', '', vietnamese_transcript[idx]).strip()
                break
                
        # If no keyword match, try exact choice text matching
        if not best_matching_sentence:
            for idx, line in enumerate(transcript):
                line_clean = re.sub(r'^[A-Za-z]+[-A-Za-z]*\s*:\s*', '', line).strip()
                if correct_choice_text.lower() in line_clean.lower():
                    best_matching_sentence = line_clean
                    if idx < len(vietnamese_transcript):
                        best_matching_viet_sentence = re.sub(r'^[A-Za-z]+[-A-Za-z]*\s*:\s*', '', vietnamese_transcript[idx]).strip()
                    break

    # Build the HTML explanation card content
    explanation_html = f"<strong style='color: var(--success);'>ĐÁP ÁN ĐÚNG LÀ {answer}</strong>"
    if translated_choice_text:
        explanation_html += f" (<em>{translated_choice_text}</em>)"
    explanation_html += ".<br>"
    
    if best_matching_sentence:
        explanation_html += f"<div style='margin-top: 8px; border-left: 3px solid var(--color-cyan); padding-left: 10px; background: rgba(0, 242, 254, 0.02); padding-top: 4px; padding-bottom: 4px;'>"
        explanation_html += f"<strong>Từ khóa trong bài nghe:</strong><br>"
        explanation_html += f"<span style='color: var(--text-main); font-weight: 500;'>\"{best_matching_sentence}\"</span>"
        if best_matching_viet_sentence:
            explanation_html += f"<br><span style='color: var(--text-muted); font-size: 0.9rem;'>→ \"{best_matching_viet_sentence}\"</span>"
        explanation_html += f"</div>"
    else:
        explanation_html += f"<div style='margin-top: 8px; color: var(--text-secondary);'>Giải thích: Dựa vào nội dung cuộc hội thoại, người nói trao đổi thông tin phù hợp với phương án {answer}.</div>"
        
    return explanation_html

def process_database():
    if not os.path.exists(DATA_FILE):
        print(f"Data file {DATA_FILE} not found!")
        return
        
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print("Translating and compiling explanations...")
    
    total_sections = len(data)
    for s_idx, section in enumerate(data):
        print(f"[{s_idx+1}/{total_sections}] Processing Section: {section['title']}...")
        
        # Translate section description/notes if overview or tips
        if section.get("theory"):
            for slide in section["theory"]:
                translated_text = []
                for t in slide.get("text", []):
                    translated_text.append(translate_text(t))
                slide["vietnamese_text"] = translated_text
                
        if section.get("vocabulary"):
            for slide in section["vocabulary"]:
                if not slide.get("vietnamese_text"):
                    translated_text = []
                    for t in slide.get("text", []):
                        translated_text.append(translate_text(t))
                    slide["vietnamese_text"] = translated_text

        # 1. Translate Examples
        if section.get("examples"):
            for ex in section["examples"]:
                if ex.get("questions"):
                    # Example set (for topics)
                    # Translate set transcript
                    ex_viet_transcript = [translate_text(line) for line in ex.get("transcript", [])]
                    ex["vietnamese_transcript"] = ex_viet_transcript
                    
                    for q in ex["questions"]:
                        q["vietnamese_question"] = translate_text(q["question"])
                        v_choices = {}
                        for key, text in q.get("choices", {}).items():
                            v_choices[key] = translate_text(text)
                        q["vietnamese_choices"] = v_choices
                        
                        # Generate explanation
                        q["explanation"] = generate_explanation(
                            q["question"], q["choices"], q["answer"], 
                            ex.get("transcript", []), v_choices, ex_viet_transcript
                        )
                else:
                    # Single example
                    ex["vietnamese_question"] = translate_text(ex["question"])
                    v_choices = {}
                    for key, text in ex.get("choices", {}).items():
                        v_choices[key] = translate_text(text)
                    ex["vietnamese_choices"] = v_choices
                    
                    ex_viet_transcript = [translate_text(line) for line in ex.get("transcript", [])]
                    ex["vietnamese_transcript"] = ex_viet_transcript
                    
                    ex["explanation"] = generate_explanation(
                        ex["question"], ex["choices"], ex["answer"],
                        ex.get("transcript", []), v_choices, ex_viet_transcript
                    )

        # 2. Translate Practice Questions (Single questions)
        if section.get("practice"):
            for q in section["practice"]:
                q["vietnamese_question"] = translate_text(q["question"])
                v_choices = {}
                for key, text in q.get("choices", {}).items():
                    v_choices[key] = translate_text(text)
                q["vietnamese_choices"] = v_choices
                
                q_viet_transcript = [translate_text(line) for line in q.get("transcript", [])]
                q["vietnamese_transcript"] = q_viet_transcript
                
                q["explanation"] = generate_explanation(
                    q["question"], q["choices"], q["answer"],
                    q.get("transcript", []), v_choices, q_viet_transcript
                )

        # 3. Translate Practice Sets (For topics)
        if section.get("practice_sets"):
            for p_set in section["practice_sets"]:
                p_viet_transcript = [translate_text(line) for line in p_set.get("transcript", [])]
                p_set["vietnamese_transcript"] = p_viet_transcript
                
                for q in p_set["questions"]:
                    q["vietnamese_question"] = translate_text(q["question"])
                    v_choices = {}
                    for key, text in q.get("choices", {}).items():
                        v_choices[key] = translate_text(text)
                    q["vietnamese_choices"] = v_choices
                    
                    q["explanation"] = generate_explanation(
                        q["question"], q["choices"], q["answer"],
                        p_set.get("transcript", []), v_choices, p_viet_transcript
                    )
                    
    # Save cache
    save_cache()
    
    # Save back to JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Updated data saved to {OUTPUT_FILE}")
    
    # Save back to JS data file
    with open(JS_OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("window.part03Data = ")
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write(";")
    print(f"Updated JS saved to {JS_OUTPUT_FILE}")

if __name__ == "__main__":
    process_database()
