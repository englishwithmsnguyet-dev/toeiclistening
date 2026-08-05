import json
import re

with open("data/part01_data.js", "r", encoding="utf-8") as f:
    content = f.read()

start_idx = content.find("[")
end_idx = content.rfind("]") + 1
data = json.loads(content[start_idx:end_idx])

for section in data:
    if section["id"] == "dang_03":
        for slide in section.get("theory", []):
            idx = slide.get("slide_index")
            
            # Formatting Slides 30-35 (Grammar Structures)
            if 30 <= idx <= 35:
                text_lines = slide["text"]
                
                # Extract parts
                struct_title = text_lines[0]
                # clean up HTML in title
                struct_title_clean = re.sub(r'<[^>]+>', '', struct_title)
                
                struct_formula = text_lines[1]
                
                examples = []
                notes = []
                in_examples = False
                in_notes = False
                
                for line in text_lines[2:]:
                    clean_line = re.sub(r'<[^>]+>', '', line).strip()
                    if clean_line.upper().startswith("VÍ DỤ"):
                        in_examples = True
                        in_notes = False
                        continue
                    elif clean_line.startswith("→") or "→" in clean_line or line.startswith("<span"):
                        # In slide 33, note starts with →, then next lines start with <span style="color: #00B0F0;"><strong>V3ed...
                        in_examples = False
                        in_notes = True
                    
                    if in_examples:
                        examples.append(line)
                    elif in_notes:
                        notes.append(line)
                
                # Build beautiful HTML
                html = []
                html.append(f'''<div style="background: #f0fdf4; border-left: 4px solid #00B050; padding: 16px; margin-bottom: 20px; border-radius: 4px;">
  <div style="color: #00B050; font-weight: bold; font-size: 1.2rem; margin-bottom: 8px;">{struct_title_clean}</div>
  <div style="font-size: 1.4rem; color: #333;">{struct_formula}</div>
</div>''')

                if examples:
                    examples_html = ''.join([f'<div style="margin-bottom: 8px; padding-left: 12px; border-left: 2px solid #cbd5e1; font-size: 1.2rem;">{ex}</div>' for ex in examples])
                    html.append(f'''<div style="background: #f8fafc; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
  <div style="font-weight: bold; color: #475569; margin-bottom: 12px; font-size: 1.1rem;">VÍ DỤ:</div>
  {examples_html}
</div>''')

                if notes:
                    notes_html = '<br>'.join(notes)
                    html.append(f'''<div style="background: #fffbeb; padding: 16px; border-radius: 8px; color: #b45309; font-size: 1.1rem;">
  <span style="font-weight: bold;">💡 Lưu ý:</span><br>{notes_html}
</div>''')

                slide["text"] = html

            # Formatting Slide 36 (Practice Title)
            elif idx == 36:
                slide["text"] = [
                  "<span style=\"color: #FF0000;\"><strong>BÀI TẬP </strong></span>",
                  "<span style=\"color: #FF0000;\"><strong>ÁP DỤNG</strong></span>"
                ]

            # Formatting Slides 37-52 (Practice Quizzes)
            elif 37 <= idx <= 52:
                if "practice" not in slide:
                    options = []
                    for t in slide.get("text", []):
                        # Remove (A), (B), (C), (D) from the beginning
                        # We replace the literal text but keep the styling if it's outside.
                        # Since the raw string might be like: <span style="color: #0070C0;">(A) The cars </span>
                        # We just regex replace "(A) ", "(B) ", etc.
                        clean_t = re.sub(r'\([A-D]\)\s*', '', t, count=1)
                        options.append(clean_t)
                    
                    slide["text"] = []
                    slide["practice"] = {
                        "options": options,
                        "answer": "",
                        "vocab": []
                    }

new_content = "window.part01Data = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n"
with open("data/part01_data.js", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Done refactoring dang_03.")
