import sys

with open('js/app.js', 'r') as f:
    code = f.read()

p1_load = '''
    function loadSectionP1(sectionId) {
        if (!window.part01Data) return;
        const sectionData = window.part01Data.find(s => s.id === sectionId);
        if (!sectionData) return;

        state.part01ActiveSection = sectionId;
        
        // Update active in submenu
        document.querySelectorAll(".submenu-item").forEach(item => {
            if (item.getAttribute("data-id") === sectionId) {
                item.classList.add("active");
                let parentSubmenu = item.closest(".part1-collapsible-submenu");
                if (parentSubmenu) {
                    parentSubmenu.style.display = "block";
                    if (part1ExpandIcon) part1ExpandIcon.innerHTML = `<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m18 15-6-6-6 6"/></svg>`;
                }
            } else {
                item.classList.remove("active");
            }
        });

        // Setup Header
        part1Panel.innerHTML = `
            <div class="panel-header">
                <div class="breadcrumbs">
                    <span>PART 01: PHOTOGRAPHS</span> &nbsp;/&nbsp; <span>${sectionData.type === 'test' ? 'LUYỆN TẬP ETS 2026' : 'DẠNG CÂU HỎI'}</span>
                </div>
                <h3 id="panel-title-p1">${sectionData.title}</h3>
            </div>
            <div id="p1-content-area" style="padding: 24px;"></div>
        `;
        
        const contentArea = document.getElementById("p1-content-area");

        if (sectionData.type === "theory" || sectionData.type === "overview") {
            renderTheoryP1(sectionData.theory, contentArea);
        } else if (sectionData.type === "test") {
            renderTestP1(sectionData, contentArea);
        }
    }

    function renderTheoryP1(slides, container) {
        if (!slides || slides.length === 0) {
            container.innerHTML = "<p>Nội dung đang được cập nhật...</p>";
            return;
        }

        let html = `<div class="theory-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 24px;">`;
        
        slides.forEach(slide => {
            let imgHtml = '';
            if (slide.images && slide.images.length > 0) {
                imgHtml = `<div class="slide-images" style="margin-bottom: 16px;">`;
                slide.images.forEach(img => {
                    imgHtml += `<img src="data/graphics/part01/${img}" alt="Slide Image" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 8px;">`;
                });
                imgHtml += `</div>`;
            }
            
            let audioHtml = '';
            if (slide.audio) {
                audioHtml = `
                    <div style="margin-top: 16px; background: rgba(0,0,0,0.02); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
                        <div style="font-size: 0.8rem; font-weight: 600; color: var(--text-muted); margin-bottom: 8px; text-transform: uppercase;">Nghe ví dụ:</div>
                        <audio controls style="width: 100%; height: 36px; outline: none;">
                            <source src="media/${slide.audio}" type="audio/mpeg">
                        </audio>
                    </div>
                `;
            }
            
            html += `
                <div class="theory-card" style="background: white; border-radius: 12px; padding: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid var(--border); display: flex; flex-direction: column;">
                    ${imgHtml}
                    <div class="slide-text" style="font-size: 1.05rem; line-height: 1.6; color: var(--text-main); flex-grow: 1;">
                        ${slide.text.map(t => `<p style="margin-bottom: 8px;">${t}</p>`).join('')}
                    </div>
                    ${audioHtml}
                </div>
            `;
        });
        
        html += `</div>`;
        container.innerHTML = html;
    }

    function renderTestP1(testData, container) {
        if (!testData.practice_sets || testData.practice_sets.length === 0) {
            container.innerHTML = "<p>Đề thi đang được cập nhật...</p>";
            return;
        }

        let html = `<div class="practice-sets-container" style="display: flex; flex-direction: column; gap: 32px; max-width: 800px; margin: 0 auto;">`;
        
        testData.practice_sets.forEach((set, setIndex) => {
            const q = set.questions[0]; // Part 1 has 1 question per set
            const qId = `p1_q_${q.id}`;
            const savedAns = state.answeredQuestions[qId] || null;
            
            let choicesHtml = '';
            ['A', 'B', 'C', 'D'].forEach(opt => {
                const isSelected = savedAns === opt;
                const isCorrect = q.answer === opt;
                
                let btnClass = "choice-btn";
                if (savedAns) {
                    btnClass += " answered";
                    if (isSelected && !isCorrect) btnClass += " incorrect";
                    if (isCorrect) btnClass += " correct";
                }
                
                choicesHtml += `
                    <button class="${btnClass}" data-q="${q.id}" data-opt="${opt}" ${savedAns ? 'disabled' : ''}>
                        <span class="choice-letter">${opt}</span>
                        <span class="choice-text" style="text-align: left;">${q.choices[opt] || ""}</span>
                    </button>
                `;
            });
            
            html += `
                <div class="practice-set-card" style="background: white; border-radius: 16px; box-shadow: 0 4px 24px rgba(0,0,0,0.04); border: 1px solid var(--border); overflow: hidden;">
                    <div style="padding: 16px 24px; background: var(--bg-alt); border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0; font-size: 1.1rem; color: var(--color-cyan);">Question ${q.id}</h4>
                        <div class="audio-player-wrapper" style="width: 250px;">
                            <audio controls style="width: 100%; height: 32px; outline: none;">
                                <source src="media/${set.audio}" type="audio/mpeg">
                            </audio>
                        </div>
                    </div>
                    
                    <div style="padding: 24px; display: grid; grid-template-columns: 1fr; gap: 24px;">
                        <div class="p1-image-container" style="display: flex; justify-content: center; background: #f8fafc; padding: 16px; border-radius: 12px; border: 1px solid var(--border);">
                            <img src="data/graphics/${set.image}" alt="Question ${q.id}" style="max-width: 100%; max-height: 400px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                        </div>
                        
                        <div class="choices-grid">
                            ${choicesHtml}
                        </div>
                        
                        <div id="feedback-${q.id}" class="feedback-area" style="display: ${savedAns ? 'block' : 'none'}; padding: 16px; border-radius: 8px; background: rgba(0,0,0,0.02); border: 1px solid var(--border); margin-top: 16px;">
                            ${savedAns ? q.explanation : ''}
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += `</div>`;
        container.innerHTML = html;
        
        // Attach event listeners for choices
        const choiceBtns = container.querySelectorAll(".choice-btn");
        choiceBtns.forEach(btn => {
            btn.addEventListener("click", function() {
                if (this.classList.contains("answered")) return;
                
                const qId = parseInt(this.getAttribute("data-q"));
                const selectedOpt = this.getAttribute("data-opt");
                
                // Find the question object
                const set = testData.practice_sets.find(s => s.questions[0].id === qId);
                const qObj = set.questions[0];
                
                const globalQId = `p1_q_${qId}`;
                state.answeredQuestions[globalQId] = selectedOpt;
                
                // Save progress
                try {
                    localStorage.setItem("toeic_answered_questions", JSON.stringify(state.answeredQuestions));
                } catch(e) {}
                updateRouteProgress();
                
                // Update UI for this question block only
                const qBlock = this.closest(".practice-set-card");
                const btns = qBlock.querySelectorAll(".choice-btn");
                btns.forEach(b => {
                    b.classList.add("answered");
                    b.disabled = true;
                    const opt = b.getAttribute("data-opt");
                    if (opt === qObj.answer) {
                        b.classList.add("correct");
                    }
                    if (opt === selectedOpt && selectedOpt !== qObj.answer) {
                        b.classList.add("incorrect");
                    }
                });
                
                // Show feedback
                const feedbackEl = document.getElementById(`feedback-${qId}`);
                if (feedbackEl) {
                    feedbackEl.innerHTML = qObj.explanation;
                    feedbackEl.style.display = "block";
                }
            });
        });
    }
'''

if 'function loadSectionP1' not in code:
    code = code.replace('function loadSectionP4(id) {', p1_load + '\n    function loadSectionP4(id) {')

with open('js/app.js', 'w') as f:
    f.write(code)
print('Patch 4 done.')
