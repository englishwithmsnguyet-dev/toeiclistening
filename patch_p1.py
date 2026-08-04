import sys
import re

with open('js/app.js', 'r') as f:
    code = f.read()

# 1. Add state for part 1
code = code.replace('        // Part 2 state', '        // Part 1 state\n        part01ActiveSection: "overview",\n        part01CurrentSlide: 1,\n        part01TotalSlides: 1,\n        part01SlidesData: [],\n\n        // Part 2 state')

# 2. Rewrite renderTheoryP1 and renderTestP1 and loadSectionP1
p1_functions = '''
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
            state.part01SlidesData = sectionData.theory || [];
            state.part01TotalSlides = state.part01SlidesData.length;
            state.part01CurrentSlide = 1;
            renderTheoryP1(contentArea);
        } else if (sectionData.type === "test") {
            renderTestP1(sectionData, contentArea);
        }
    }

    function renderTheoryP1(container) {
        if (!state.part01SlidesData || state.part01SlidesData.length === 0) {
            container.innerHTML = "<p>Nội dung đang được cập nhật...</p>";
            return;
        }

        // Generate slide carousel UI
        container.innerHTML = `
            <div class="theory-carousel-container" style="background: white; border-radius: 12px; padding: 24px; box-shadow: 0 4px 24px rgba(0,0,0,0.03); border: 1px solid var(--border); display: flex; flex-direction: column; min-height: 500px;">
                <div id="p1-slide-content" style="flex-grow: 1;">
                    <!-- Slide content rendered here -->
                </div>
                
                <div class="slide-controls" style="display: flex; justify-content: space-between; align-items: center; margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--border);">
                    <button id="p1-slide-prev" class="btn" style="display: flex; align-items: center; gap: 8px; padding: 8px 16px; background: var(--bg-alt); border: 1px solid var(--border); border-radius: 6px; cursor: pointer;">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg> LÙI LẠI
                    </button>
                    <div style="font-weight: 600; color: var(--text-muted); font-size: 0.95rem;">
                        SLIDE <span id="p1-slide-current">${state.part01CurrentSlide}</span> / <span id="p1-slide-total">${state.part01TotalSlides}</span>
                    </div>
                    <button id="p1-slide-next" class="btn" style="display: flex; align-items: center; gap: 8px; padding: 8px 16px; background: linear-gradient(135deg, var(--color-cyan), var(--color-purple)); color: white; border: none; border-radius: 6px; cursor: pointer;">
                        TIẾP TỤC <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6 6 6"/></svg>
                    </button>
                </div>
            </div>
        `;
        
        updatePart01SlideView();
        
        document.getElementById("p1-slide-prev").addEventListener("click", () => {
            if (state.part01CurrentSlide > 1) {
                state.part01CurrentSlide--;
                updatePart01SlideView();
            }
        });
        
        document.getElementById("p1-slide-next").addEventListener("click", () => {
            if (state.part01CurrentSlide < state.part01TotalSlides) {
                state.part01CurrentSlide++;
                updatePart01SlideView();
            }
        });
    }
    
    function updatePart01SlideView() {
        const slide = state.part01SlidesData[state.part01CurrentSlide - 1];
        if (!slide) return;
        
        const contentContainer = document.getElementById("p1-slide-content");
        document.getElementById("p1-slide-current").innerText = state.part01CurrentSlide;
        
        const prevBtn = document.getElementById("p1-slide-prev");
        const nextBtn = document.getElementById("p1-slide-next");
        prevBtn.style.opacity = state.part01CurrentSlide === 1 ? "0.5" : "1";
        prevBtn.style.cursor = state.part01CurrentSlide === 1 ? "not-allowed" : "pointer";
        nextBtn.style.opacity = state.part01CurrentSlide === state.part01TotalSlides ? "0.5" : "1";
        nextBtn.style.cursor = state.part01CurrentSlide === state.part01TotalSlides ? "not-allowed" : "pointer";
        
        let imgHtml = '';
        let hasImage = false;
        if (slide.images && slide.images.length > 0) {
            hasImage = true;
            imgHtml = `<div class="slide-images" style="flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #f8fafc; border-radius: 12px; padding: 16px; border: 1px solid var(--border);">`;
            slide.images.forEach(img => {
                imgHtml += `<img src="data/graphics/part01/${img}" alt="Slide Image" style="max-width: 100%; max-height: 400px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 8px;">`;
            });
            imgHtml += `</div>`;
        }
        
        let audioHtml = '';
        if (slide.audio) {
            audioHtml = `
                <div style="margin-top: 24px; background: rgba(0,0,0,0.02); padding: 16px; border-radius: 8px; border: 1px solid var(--border);">
                    <div style="font-size: 0.8rem; font-weight: 600; color: var(--text-muted); margin-bottom: 12px; text-transform: uppercase; display: flex; align-items: center; gap: 6px;">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>
                        Nghe Audio:
                    </div>
                    <audio controls style="width: 100%; height: 40px; outline: none;">
                        <source src="media/${slide.audio}" type="audio/mpeg">
                    </audio>
                </div>
            `;
        }
        
        const textHtml = `
            <div class="slide-text" style="flex: 1; font-size: 1.1rem; line-height: 1.7; color: var(--text-main); display: flex; flex-direction: column;">
                <div style="flex-grow: 1;">
                    ${slide.text.map(t => `<p style="margin-bottom: 12px;">${t}</p>`).join('')}
                </div>
                ${audioHtml}
            </div>
        `;
        
        if (hasImage) {
            contentContainer.innerHTML = `
                <div style="display: flex; flex-direction: row; gap: 32px; flex-wrap: wrap;">
                    ${imgHtml}
                    ${textHtml}
                </div>
            `;
        } else {
            contentContainer.innerHTML = `
                <div style="display: flex; flex-direction: column;">
                    ${textHtml}
                </div>
            `;
        }
    }

    function renderTestP1(testData, container) {
        if (!testData.practice_sets || testData.practice_sets.length === 0) {
            container.innerHTML = "<p>Đề thi đang được cập nhật...</p>";
            return;
        }

        let html = `<div class="practice-sets-container" style="display: flex; flex-direction: column; gap: 32px;">`;
        
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
                    <button class="${btnClass}" data-q="${q.id}" data-opt="${opt}" ${savedAns ? 'disabled' : ''} style="display: flex; align-items: center; padding: 14px 16px; border: 1px solid var(--border); border-radius: 8px; background: var(--bg-card); cursor: pointer; transition: var(--transition); width: 100%; text-align: left; margin-bottom: 12px;">
                        <span class="choice-letter" style="flex-shrink: 0; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; background: rgba(0,0,0,0.05); border-radius: 50%; font-weight: 700; margin-right: 12px;">${opt}</span>
                        <span class="choice-text" style="flex-grow: 1; font-weight: 500;">${q.choices[opt] || ""}</span>
                    </button>
                `;
            });
            
            html += `
                <div class="practice-set-card" style="background: white; border-radius: 16px; box-shadow: 0 8px 30px rgba(0,0,0,0.04); border: 1px solid var(--border); overflow: hidden;">
                    <div style="padding: 16px 24px; background: linear-gradient(90deg, rgba(0,242,254,0.05), rgba(168,85,247,0.05)); border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0; font-size: 1.2rem; font-weight: 700; color: var(--color-cyan);">Question ${q.id}</h4>
                    </div>
                    
                    <div style="padding: 24px; display: flex; flex-direction: row; gap: 32px; flex-wrap: wrap;">
                        <!-- Left Column: Image -->
                        <div class="p1-image-container" style="flex: 1.5; min-width: 300px; display: flex; justify-content: center; align-items: center; background: #f8fafc; padding: 16px; border-radius: 12px; border: 1px solid var(--border);">
                            <img src="data/graphics/${set.image}" alt="Question ${q.id}" style="max-width: 100%; max-height: 450px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08);">
                        </div>
                        
                        <!-- Right Column: Audio & Choices -->
                        <div class="p1-content-container" style="flex: 1; min-width: 300px; display: flex; flex-direction: column;">
                            <div class="audio-player-wrapper" style="margin-bottom: 24px; background: rgba(0,0,0,0.02); padding: 16px; border-radius: 12px; border: 1px solid var(--border);">
                                <div style="font-size: 0.8rem; font-weight: 600; color: var(--text-muted); margin-bottom: 8px; text-transform: uppercase;">Listen & Choose:</div>
                                <audio controls style="width: 100%; height: 40px; outline: none;">
                                    <source src="media/${set.audio}" type="audio/mpeg">
                                </audio>
                            </div>
                            
                            <div class="choices-grid">
                                ${choicesHtml}
                            </div>
                            
                            <div id="feedback-${q.id}" class="feedback-area" style="display: ${savedAns ? 'block' : 'none'}; padding: 16px; border-radius: 8px; background: rgba(168,85,247,0.05); border: 1px solid rgba(168,85,247,0.2); margin-top: 16px;">
                                ${savedAns ? q.explanation : ''}
                            </div>
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
                        b.style.background = "var(--success-bg)";
                        b.style.borderColor = "var(--success)";
                    }
                    if (opt === selectedOpt && selectedOpt !== qObj.answer) {
                        b.classList.add("incorrect");
                        b.style.background = "var(--danger-bg)";
                        b.style.borderColor = "var(--danger)";
                    }
                });
                
                // Show feedback
                const feedbackEl = document.getElementById(`feedback-${qId}`);
                if (feedbackEl) {
                    feedbackEl.innerHTML = qObj.explanation;
                    feedbackEl.style.display = "block";
                }
                
                if (selectedOpt === qObj.answer) {
                    spawnConfetti(20, true);
                    playCorrect();
                } else {
                    playIncorrect();
                }
            });
        });
    }
'''

# Use regex to find and replace loadSectionP1, renderTheoryP1, and renderTestP1 block
# The block starts at `function loadSectionP1(sectionId) {` and ends before `function togglePart1Submenu(expand) {`
# Wait, let's use exact match or regex
pattern = re.compile(r'function loadSectionP1\(sectionId\) \{.*?function togglePart1Submenu\(expand\) \{', re.DOTALL)
if pattern.search(code):
    code = pattern.sub(p1_functions + '\n    function togglePart1Submenu(expand) {', code)
else:
    print("Could not find the block to replace!")
    sys.exit(1)

with open('js/app.js', 'w') as f:
    f.write(code)
print("UI patched successfully.")
