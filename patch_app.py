import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Add the global functions first
global_funcs = """
window.selectPracticeOption = function(el) {
    if (el.parentElement.hasAttribute('data-checked')) return;
    const siblings = el.parentElement.querySelectorAll('.practice-option');
    siblings.forEach(s => {
        s.style.backgroundColor = '';
        s.style.borderColor = 'var(--border)';
        s.classList.remove('selected');
    });
    el.style.backgroundColor = '#f0f9ff';
    el.style.borderColor = '#0284c7';
    el.classList.add('selected');
};

window.checkPracticeAnswer = function(btn) {
    const container = document.getElementById('practice-options-container');
    const selected = container.querySelector('.practice-option.selected');
    if (!selected) {
        alert("Vui lòng chọn một đáp án trước khi kiểm tra!");
        return;
    }
    
    if (container.hasAttribute('data-checked')) return;
    container.setAttribute('data-checked', 'true');
    btn.style.opacity = '0.5';
    btn.style.cursor = 'not-allowed';
    
    const options = container.querySelectorAll('.practice-option');
    options.forEach(opt => {
        const isCorrect = opt.getAttribute('data-correct') === 'true';
        if (isCorrect) {
            opt.style.backgroundColor = '#dcfce7';
            opt.style.borderColor = '#16a34a';
            opt.innerHTML = opt.innerHTML.replace('</strong>', '</strong> <span style="color: #16a34a;">✔️</span>');
        } else if (opt === selected && !isCorrect) {
            opt.style.backgroundColor = '#fee2e2';
            opt.style.borderColor = '#dc2626';
            opt.innerHTML = opt.innerHTML.replace('</strong>', '</strong> <span style="color: #dc2626;">❌</span>');
        }
    });
};

"""

# Prepend the global funcs at the start (or anywhere globally accessible)
if "window.selectPracticeOption" not in content:
    content = global_funcs + content

# Replace inside updatePart01SlideView
target_start = "let hasImage = slide.images && slide.images.length > 0;"

new_block = """
        if (slide.practice) {
            const p = slide.practice;
            const imgPath = slide.images && slide.images.length > 0 ? `data/graphics/part01/${slide.images[0]}` : '';
            
            let optionsHtml = '';
            const labels = ['A', 'B', 'C', 'D'];
            p.options.forEach((opt, i) => {
                const isCorrect = labels[i] === p.answer;
                optionsHtml += `
                    <div class="practice-option" data-correct="${isCorrect}" style="padding: 12px 16px; border: 1px solid var(--border); border-radius: 8px; margin-bottom: 12px; cursor: pointer; transition: all 0.2s;" onclick="selectPracticeOption(this)">
                        <strong style="margin-right: 8px; font-size: 1.1em;">${labels[i]}.</strong> <span>${opt}</span>
                    </div>
                `;
            });
            
            let vocabHtml = '';
            p.vocab.forEach(v => {
                vocabHtml += `
                    <div style="display: flex; gap: 8px; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px dashed #e2e8f0; font-size: 1.15rem;">
                        <span style="font-weight: 600; color: #0284c7; min-width: 140px; display: inline-block;">${v.en}</span>
                        <span style="color: var(--text-main);">- ${v.vi}</span>
                    </div>
                `;
            });

            contentContainer.innerHTML = `
                <div style="display: flex; flex-direction: row; gap: 40px; flex-wrap: nowrap; align-items: stretch; justify-content: center; width: 100%;">
                    <div style="flex: 1; max-width: 45%; display: flex; justify-content: center; align-items: flex-start;">
                        <img src="${imgPath}" alt="Practice Image" style="width: 100%; max-height: 450px; object-fit: contain; border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.08);">
                    </div>
                    <div style="flex: 1; min-width: 300px; max-width: 55%; font-size: 1.25rem; line-height: 1.6; color: var(--text-main); display: flex; flex-direction: column;">
                        <div id="practice-options-container" style="margin-bottom: 24px;">
                            ${optionsHtml}
                        </div>
                        <div style="display: flex; gap: 16px; margin-bottom: 24px;">
                            <button onclick="checkPracticeAnswer(this)" style="background: var(--primary); color: white; border: none; padding: 12px 32px; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 1.1rem; box-shadow: 0 4px 12px rgba(37,99,235,0.2); transition: all 0.2s;" onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'">Kiểm tra</button>
                        </div>
                        <details style="cursor: pointer; background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 16px;">
                          <summary style="font-weight: bold; color: #16a34a; outline: none; list-style-type: '👉 '; font-size: 1.15rem;">Hiển thị từ vựng</summary>
                          <div style="margin-top: 16px;">
                            ${vocabHtml}
                          </div>
                        </details>
                    </div>
                </div>
            `;
        } else {
"""

# I need to match the block starting from hasImage up to the end of the if-else for textHtml.
# The easiest way is to inject `if (slide.practice) { ... } else { ...original logic... }`
# I'll replace `let hasImage = slide.images && slide.images.length > 0;` with `let hasImage ... \n if (slide.practice) ... else {`
# And add `}` right before `prevBtn.style.opacity`

end_target = 'prevBtn.style.opacity = state.part01CurrentSlide === 1 ? "0.4" : "1";'

parts = content.split(target_start)
if len(parts) == 2:
    sub_parts = parts[1].split(end_target)
    if len(sub_parts) == 2:
        new_content = parts[0] + new_block + "            let hasImage = slide.images && slide.images.length > 0;\n" + sub_parts[0] + "        }\n\n        " + end_target + sub_parts[1]
        with open('js/app.js', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Patched app.js successfully!")
    else:
        print("Could not find end_target")
else:
    print("Could not find target_start")

