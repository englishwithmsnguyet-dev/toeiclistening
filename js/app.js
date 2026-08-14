

window.playTTS = function(text, event) {
    if (event) event.stopPropagation(); // prevent triggering row click
    
    // Remove phonetic symbols or html tags if any are left
    text = text.replace(/<[^>]+>/g, '').replace(/\/[^\/]+\//g, '').trim();

    if (!('speechSynthesis' in window)) {
        alert("Trình duyệt của bạn không hỗ trợ tính năng đọc từ vựng.");
        return;
    }
    
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    
    const setVoiceAndPlay = () => {
        const voices = window.speechSynthesis.getVoices();
        let bestVoice = voices.find(v => v.lang === 'en-US' && (v.name.includes('Google') || v.name.includes('Samantha') || v.name.includes('Microsoft')));
        if (!bestVoice) bestVoice = voices.find(v => v.lang.startsWith('en-'));
        if (bestVoice) utterance.voice = bestVoice;
        
        utterance.rate = 0.9;
        utterance.pitch = 1.0;
        window.speechSynthesis.speak(utterance);
    };

    if (window.speechSynthesis.getVoices().length === 0) {
        window.speechSynthesis.onvoiceschanged = setVoiceAndPlay;
    } else {
        setVoiceAndPlay();
    }
};

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

// -------------------------------------------------------------
// TOEIC Listening Platform - Core Application Logic
// Inspired by the Approved TOEIC Reading Premium Styling & Mechanics
// -------------------------------------------------------------

document.addEventListener("DOMContentLoaded", () => {
    // Web Audio API Sound Effects Helper
    const SoundEffects = {
        audioCtx: null,

        init() {
            if (!this.audioCtx) {
                this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
        },

        playCorrect() {
            this.init();
            if (this.audioCtx.state === 'suspended') {
                this.audioCtx.resume();
            }
            
            const now = this.audioCtx.currentTime;
            
            // Osc 1: First high note
            const osc1 = this.audioCtx.createOscillator();
            const gain1 = this.audioCtx.createGain();
            osc1.type = 'sine';
            osc1.frequency.setValueAtTime(523.25, now); // C5
            
            gain1.gain.setValueAtTime(0, now);
            gain1.gain.linearRampToValueAtTime(0.15, now + 0.05);
            gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
            
            osc1.connect(gain1);
            gain1.connect(this.audioCtx.destination);
            
            // Osc 2: Second higher note (chime effect)
            const osc2 = this.audioCtx.createOscillator();
            const gain2 = this.audioCtx.createGain();
            osc2.type = 'sine';
            osc2.frequency.setValueAtTime(659.25, now + 0.08); // E5
            
            gain2.gain.setValueAtTime(0, now + 0.08);
            gain2.gain.linearRampToValueAtTime(0.15, now + 0.12);
            gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.45);
            
            osc2.connect(gain2);
            gain2.connect(this.audioCtx.destination);
            
            osc1.start(now);
            osc1.stop(now + 0.3);
            osc2.start(now + 0.08);
            osc2.stop(now + 0.45);
        },

        playWrong() {
            this.init();
            if (this.audioCtx.state === 'suspended') {
                this.audioCtx.resume();
            }
            
            const now = this.audioCtx.currentTime;
            
            const osc = this.audioCtx.createOscillator();
            const gain = this.audioCtx.createGain();
            osc.type = 'triangle';
            
            // Descending frequency for a soft buzzer/thud
            osc.frequency.setValueAtTime(150, now);
            osc.frequency.linearRampToValueAtTime(100, now + 0.25);
            
            gain.gain.setValueAtTime(0, now);
            gain.gain.linearRampToValueAtTime(0.2, now + 0.05);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
            
            osc.connect(gain);
            gain.connect(this.audioCtx.destination);
            
            osc.start(now);
            osc.stop(now + 0.3);
        }
    };
    const LOCKED_SECTIONS = [
        "yn_basic", "yn_embedded", "yn_negative", "yn_tag", "info_how", "info_what", "info_when", "info_where", "info_who", "info_why", "choice_questions", "statements", "suggestions_invitations", "ets_test_01", "ets_test_02", "ets_test_03", "ets_test_04", "ets_test_05",
        "dang_01_identity", "dang_01_location", "dang_01_topic", "dang_02_problem", "dang_02_what_according", "dang_02_what_do_next", "dang_02_what_imply", "dang_02_what_request", "dang_02_what_say", "dang_02_what_suggest", "dang_02_why", "dang_visual_questions",
        "topic_01", "topic_02", "topic_03", "topic_04", "topic_05", "topic_06"
    ];

    // App State
    const state = {
        activeView: "home",
        part03Data: null,
        part04Data: null,
        part03ActiveSection: "overview",
        part04ActiveSection: "overview", // Active category ID (e.g. 'overview', 'dang_01_topic')
        part03ActiveTab: "theory",
        part04ActiveTab: "theory", // 'theory', 'vocabulary', 'examples', 'practice'
        
        // Part 1 state
        part01ActiveSection: "overview",
        part01CurrentSlide: 1,
        part01TotalSlides: 1,
        part01SlidesData: [],
        
        // Part 2 state
        part02CurrentSlide: 1,
        part02TotalSlides: 318,
        
        // Audio state
        currentAudio: null,
        currentAudioBtn: null,
        
        // Progress tracking state
        answeredQuestions: {}, // Map of unique question key (slide_index) -> true
        
        // Quiz states
        quiz: {
            sectionId: null,
            questions: [],
            currentIdx: 0,
            score: 0,
            reviewMode: false,
            answers: {} // slide_index -> chosen option letter
        },
        setQuiz: {
            sectionId: null,
            sets: [],
            currentIdx: 0,
            completedSets: {}, // set_index -> score
            reviewMode: false,
            answers: {} // question_slide_index -> chosen option letter
        }
    };

    // --- LOCK & PASSWORD LOGIC ---
    window.isUnlocked = sessionStorage.getItem("portal_unlocked_v2") === "true";
    window.pendingUnlockCallback = null;

    window.showPaywallModal = function(callback) {
        if (window.isUnlocked) {
            if (callback) callback();
            return;
        }
        window.pendingUnlockCallback = callback;
        const modal = document.getElementById('password-modal');
        if(modal) {
            modal.classList.remove('hidden');
            modal.style.opacity = '1';
            modal.style.pointerEvents = 'auto';
            document.getElementById('passwordInput').value = '';
            document.getElementById('passwordError').style.display = 'none';
            setTimeout(() => {
                const input = document.getElementById('passwordInput');
                if(input) input.focus();
            }, 50);
        }
    };

    window.closePasswordModal = function() {
        const modal = document.getElementById('password-modal');
        if(modal) {
            modal.style.opacity = '0';
            modal.style.pointerEvents = 'none';
            setTimeout(() => modal.classList.add('hidden'), 300);
        }
    };

    // Initialize modal event listeners directly (already in DOMContentLoaded)
    const submitBtn = document.getElementById('submitPasswordBtn');
    const cancelBtn = document.getElementById('cancelPasswordBtn');
    const passInput = document.getElementById('passwordInput');
    
    if (submitBtn) {
        submitBtn.addEventListener('click', () => {
            if (passInput && (passInput.value === "missnguyet2026" || passInput.value.toLowerCase() === "quế anh")) {
                window.isUnlocked = true;
                sessionStorage.setItem("portal_unlocked_v2", "true");
                window.closePasswordModal();
                if (window.pendingUnlockCallback) window.pendingUnlockCallback();
                
                // Refresh sidebars to remove lock icons
                if (typeof initializePart01Sidebar === 'function') initializePart01Sidebar();
                if (typeof initializePart02Sidebar === 'function') initializePart02Sidebar();
                if (typeof initializePart03Sidebar === 'function') initializePart03Sidebar();
                if (typeof initializePart04Sidebar === 'function') initializePart04Sidebar();
                
                document.querySelectorAll('.dashboard-card').forEach(card => card.classList.remove('locked'));
            } else {
                const err = document.getElementById('passwordError');
                if(err) err.style.display = 'block';
            }
        });
    }
    
    if (cancelBtn) {
        cancelBtn.addEventListener('click', window.closePasswordModal);
    }
    
    if (passInput) {
        passInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') submitBtn.click();
        });
    }
    // --- END LOCK LOGIC ---


    // Inline SVG Icon Constants (Safe offline fallbacks to replace FontAwesome)
    const icons = {
        play: `<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" style="display:inline-block; vertical-align:middle;"><path d="M8 5v14l11-7z"/></svg>`,
        pause: `<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" style="display:inline-block; vertical-align:middle;"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>`,
        chevronDown: `<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor" style="display:inline-block; vertical-align:middle;"><path d="M7 10l5 5 5-5z"/></svg>`,
        chevronUp: `<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor" style="display:inline-block; vertical-align:middle;"><path d="M7 14l5-5 5 5z"/></svg>`
    };

    // Category tree mapping matching the requested structure
    const categoryTree = [
        {
            type: "item",
            id: "overview",
            title: "Tổng quan Phần 03"
        },
        {
            type: "item",
            id: "tips",
            title: "Chiến thuật làm bài"
        },
        {
            type: "group",
            title: "I. Câu hỏi bối cảnh",
            items: [
                { id: "dang_01_topic", title: "1. Chủ đề" },
                { id: "dang_01_location", title: "2. Địa điểm" },
                { id: "dang_01_identity", title: "3. Nghề nghiệp" }
            ]
        },
        {
            type: "group",
            title: "II. Câu hỏi thông tin chi tiết",
            items: [
                { id: "dang_02_problem", title: "1. Vấn đề" },
                { id: "dang_02_why", title: "2. Lý do / Mục đích" },
                { id: "dang_02_what_say", title: "3. Thông tin đề cập" },
                { id: "dang_02_what_according", title: "4. According to..." }
            ]
        },
        {
            type: "group",
            title: "III. Chức năng giao tiếp",
            items: [
                { id: "dang_02_what_request", title: "1. Yêu cầu" },
                { id: "dang_02_what_suggest", title: "2. Gợi ý / Đề xuất" }
            ]
        },
        {
            type: "group",
            title: "IV. Câu hỏi suy luận",
            items: [
                { id: "dang_02_what_do_next", title: "1. Hành động tiếp theo" },
                { id: "dang_02_what_imply", title: "2. Ngụ ý" }
            ]
        },
        {
            type: "group",
            title: "V. Kết hợp hình ảnh",
            items: [
                { id: "dang_visual_questions", title: "1. Luyện tập" }
            ]
        }
    ];

    // Category tree mapping for Part 4
    
    const categoryTreeP1 = [
        { type: "item", id: "overview", title: "Tổng quan Phần 01" },
        { type: "item", id: "dang_01", title: "Dạng 1: Tranh 1 người" },
        { type: "item", id: "dang_02", title: "Dạng 2: Tranh nhiều người" },
        { type: "item", id: "dang_03", title: "Dạng 3: Tranh mô tả vật" }
    ];

    const categoryTreeP2 = [
        { type: "item", id: "overview", title: "TỔNG QUAN PHẦN 02" },
        { 
            type: "group", 
            title: "1. INFORMATION QUESTIONS",
            items: [
                { id: "info_who", title: "Questions with Who/Whom/Whose" },
                { id: "info_where", title: "Questions with Where" },
                { id: "info_when", title: "Questions with When" },
                { id: "info_why", title: "Questions with Why" },
                { id: "info_what", title: "Questions with What" },
                { id: "info_how", title: "Questions with How" }
            ]
        },
        { 
            type: "group", 
            title: "2. YES/NO QUESTIONS",
            items: [
                { id: "yn_basic", title: "Basic Yes/No" },
                { id: "yn_negative", title: "Negative Questions" },
                { id: "yn_tag", title: "Tag Questions" },
                { id: "yn_embedded", title: "Embedded Questions" }
            ]
        },
        { type: "item", id: "choice_questions", title: "3. CHOICE QUESTIONS" },
        { type: "item", id: "suggestions_invitations", title: "4. SUGGESTIONS & INVITATIONS" },
        { type: "item", id: "statements", title: "5. STATEMENTS" }
    ];

    const categoryTreeP4 = [
        {
            type: "item",
            id: "overview",
            title: "Tổng quan Phần 04"
        },
        {
            type: "group",
            title: "CÁC CHỦ ĐỀ THƯỜNG GẶP",
            items: [
                { id: "topic_01", title: "1. Tin nhắn điện thoại" },
                { id: "topic_02", title: "2. Thông báo" },
                { id: "topic_03", title: "3. Quảng cáo" },
                { id: "topic_04", title: "4. Buổi phát thanh" },
                { id: "topic_05", title: "5. Bài diễn thuyết" },
                { id: "topic_06", title: "6. Trích đoạn cuộc họp" }
            ]
        }
    ];

    // Load progress from localStorage
    try {
        const savedProgress = localStorage.getItem("toeic_answered_questions");
        if (savedProgress) {
            state.answeredQuestions = JSON.parse(savedProgress);
        }
    } catch (e) {
        console.error("Failed to load progress:", e);
    }

    // DOM Elements
    const sidebar = document.getElementById("sidebar");
    const toggleSidebarBtn = document.getElementById("toggleSidebarBtn");
    const toggleIcon = document.getElementById("toggleIcon");
    
    const navHomeBtn = document.getElementById("navHomeBtn");
    const navPart2Btn = document.getElementById("navPart2Btn");
    const navPart3Btn = document.getElementById("navPart3Btn");
    const part3SubmenuContainer = document.getElementById("part3SubmenuContainer");
    const part3ExpandIcon = document.getElementById("part3ExpandIcon");
    
    const themeToggleBtn = document.getElementById("themeToggleBtn");
    const themeIcon = document.getElementById("themeIcon");
    const themeText = document.getElementById("themeText");
    
    const conceptsNavList = document.getElementById("concepts-nav-list");
    const topicsNavList = document.getElementById("topics-nav-list");
    
    
    // Part 1 elements

    const part1SubmenuContainer = document.getElementById("part1SubmenuContainer");
    const part1ExpandIcon = document.getElementById("part1ExpandIcon");
    const part1ConceptsNavList = document.getElementById("part1-concepts-nav-list");
    const part1TopicsNavList = document.getElementById("part1-topics-nav-list");
    
    const viewPart1 = document.getElementById("view-part1");
    const part1Panel = document.getElementById("part1-panel");

    // Part 4 elements
    const navPart4Btn = document.getElementById("navPart4Btn");
    const part4SubmenuContainer = document.getElementById("part4SubmenuContainer");
    const part4ExpandIcon = document.getElementById("part4ExpandIcon");
    const part4ConceptsNavList = document.getElementById("part4-concepts-nav-list");
    const part4TopicsNavList = document.getElementById("part4-topics-nav-list");

    const contentViews = document.querySelectorAll(".content-view");
    const mainTitleText = document.getElementById("main-title-text");

    // Part 2 elements
    const viewPart2 = document.getElementById("view-part2");
    const part2SubmenuContainer = document.getElementById("part2SubmenuContainer");
    const part2ExpandIcon = document.getElementById("part2ExpandIcon");
    const part2ConceptsNavList = document.getElementById("part2-concepts-nav-list");

    const panelTitleP2 = document.getElementById("panel-title-p2");
    const breadCurrentP2 = document.getElementById("bread-current-p2");
    const secBtnTheoryP2 = document.getElementById("sec-btn-theory-p2");
    const secBtnVocabularyP2 = document.getElementById("sec-btn-vocabulary-p2");
    const secBtnExamplesP2 = document.getElementById("sec-btn-examples-p2");
    const secBtnPracticeP2 = document.getElementById("sec-btn-practice-p2");
    
    const secTheoryP2 = document.getElementById("sec-theory-p2");
    const secVocabularyP2 = document.getElementById("sec-vocabulary-p2");
    const secExamplesP2 = document.getElementById("sec-examples-p2");
    const secPracticeP2 = document.getElementById("sec-practice-p2");
    
    const theoryContentAreaP2 = document.getElementById("theory-content-area-p2");
    const vocabularyContentAreaP2 = document.getElementById("vocabulary-content-area-p2");
    const examplesContentAreaP2 = document.getElementById("examples-content-area-p2");
    const practiceContentAreaP2 = document.getElementById("practice-content-area-p2");

    // Part 3 elements
    const breadParent = document.getElementById("bread-parent");
    const breadCurrent = document.getElementById("bread-current");
    const panelTitle = document.getElementById("panel-title");
    const panelTabBtns = document.querySelectorAll(".panel-section-btn");
    const panelTabs = document.querySelectorAll(".panel-content");
    
    const theoryContentArea = document.getElementById("theory-content-area");
    const vocabularyContentArea = document.getElementById("vocabulary-content-area");
    const examplesContentArea = document.getElementById("examples-content-area");
    const practiceContentArea = document.getElementById("practice-content-area");


    // Part 4 elements (Main View)
    const breadParentP4 = document.getElementById("bread-parent-p4");
    const breadCurrentP4 = document.getElementById("bread-current-p4");
    const panelTitleP4 = document.getElementById("panel-title-p4");
    
    const secBtnTheoryP4 = document.getElementById("sec-btn-theory-p4");
    const secBtnVocabularyP4 = document.getElementById("sec-btn-vocabulary-p4");
    const secBtnExamplesP4 = document.getElementById("sec-btn-examples-p4");
    const secBtnPracticeP4 = document.getElementById("sec-btn-practice-p4");
    
    const secTheoryP4 = document.getElementById("sec-theory-p4");
    const secVocabularyP4 = document.getElementById("sec-vocabulary-p4");
    const secExamplesP4 = document.getElementById("sec-examples-p4");
    const secPracticeP4 = document.getElementById("sec-practice-p4");
    
    const theoryContentAreaP4 = document.getElementById("theory-content-area-p4");
    const vocabularyContentAreaP4 = document.getElementById("vocabulary-content-area-p4");
    const examplesContentAreaP4 = document.getElementById("examples-content-area-p4");
    const practiceContentAreaP4 = document.getElementById("practice-content-area-p4");
    
    const panelTabBtnsP4 = document.querySelectorAll(".panel-section-btn-p4");
    const panelTabsP4 = document.querySelectorAll(".panel-content-p4");

    // Result Modal elements
    const resultModal = document.getElementById("result-modal");
    const modalScore = document.getElementById("modal-score");
    const modalTotal = document.getElementById("modal-total");
    const modalMessage = document.getElementById("modal-message");
    const modalReviewBtn = document.getElementById("modal-review-btn");
    const modalRetryBtn = document.getElementById("modal-retry-btn");

    const TOTAL_QUESTIONS_COUNT = 138;

    // Confetti Canvas Particle System
    const canvas = document.getElementById("confettiCanvas");
    const ctx = canvas.getContext("2d");
    let particles = [];
    let animationFrameId = null;

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener("resize", resizeCanvas);
    resizeCanvas();

    class ConfettiParticle {
        constructor(x, y, isGoldOnly = false) {
            this.x = x;
            this.y = y;
            this.size = Math.random() * 8 + 4;
            this.speedX = Math.random() * 10 - 5;
            this.speedY = Math.random() * -12 - 4;
            this.rotation = Math.random() * 360;
            this.rotationSpeed = Math.random() * 4 - 2;
            this.gravity = 0.25;
            
            if (isGoldOnly) {
                const goldTones = ['#ffd700', '#f59e0b', '#fbbf24', '#fef08a'];
                this.color = goldTones[Math.floor(Math.random() * goldTones.length)];
            } else {
                const colors = ['#00f2fe', '#a855f7', '#ec4899', '#3b82f6', '#10b981'];
                this.color = colors[Math.floor(Math.random() * colors.length)];
            }
        }
        
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            this.speedY += this.gravity;
            this.rotation += this.rotationSpeed;
        }
        
        draw() {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate(this.rotation * Math.PI / 180);
            ctx.fillStyle = this.color;
            ctx.fillRect(-this.size / 2, -this.size / 2, this.size, this.size);
            ctx.restore();
        }
    }

    function spawnConfetti(count = 50, isGoldOnly = false) {
        for (let i = 0; i < count; i++) {
            particles.push(new ConfettiParticle(
                canvas.width * (0.25 + Math.random() * 0.5),
                canvas.height * 0.85,
                isGoldOnly
            ));
        }
        
        if (!animationFrameId) {
            animateConfetti();
        }
    }

    function animateConfetti() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        for (let i = particles.length - 1; i >= 0; i--) {
            const p = particles[i];
            p.update();
            p.draw();
            
            // Remove offscreen
            if (p.y > canvas.height || p.x < 0 || p.x > canvas.width) {
                particles.splice(i, 1);
            }
        }
        
        if (particles.length > 0) {
            animationFrameId = requestAnimationFrame(animateConfetti);
        } else {
            cancelAnimationFrame(animationFrameId);
            animationFrameId = null;
        }
    }

    /* -------------------------------------------------------------
       1. PROGRESS TRACKING & SCORE REPORTING
       ------------------------------------------------------------- */
    function updateRouteProgress() {
        const answeredCount = Object.keys(state.answeredQuestions).length;
        const percentage = Math.min(100, Math.floor((answeredCount / TOTAL_QUESTIONS_COUNT) * 100));
        
        const percentageText = document.getElementById("progress-percentage");
        const barFill = document.getElementById("progress-bar-fill");
        
        if (percentageText) percentageText.textContent = `${percentage}%`;
        if (barFill) barFill.style.width = `${percentage}%`;
    }

    function markQuestionAnswered(questionKey) {
        state.answeredQuestions[questionKey] = true;
        updateRouteProgress();
        try {
            localStorage.setItem("toeic_answered_questions", JSON.stringify(state.answeredQuestions));
        } catch (e) {
            console.error("Failed to load progress:", e);
        }
    }

    function submitToGoogleForm(studentName, sectionTitle, typeLabel, score, total) {
        const formUrl = "https://docs.google.com/forms/d/e/1FAIpQLSfDHLX7j91RApmGiu7OT83fJ7r5outpA6-pDtrdDO_Us7x7WA/formResponse";
        const entryId = "entry.388968236";
        const reportValue = `[LISTENING] ${studentName} - ${sectionTitle} - ${typeLabel} - ${score}/${total}`;
        
        const iframe = document.createElement('iframe');
        iframe.name = 'hidden_iframe';
        iframe.style.display = 'none';
        document.body.appendChild(iframe);
        
        const form = document.createElement('form');
        form.action = formUrl;
        form.method = 'POST';
        form.target = 'hidden_iframe';
        
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = entryId;
        input.value = reportValue;
        
        form.appendChild(input);
        document.body.appendChild(form);
        form.submit();
        
        setTimeout(() => {
            document.body.removeChild(form);
            document.body.removeChild(iframe);
        }, 1000);
    }

    /* -------------------------------------------------------------
       2. VIEW SWITCHING & SUBMENU COLLAPSIBLE
       ------------------------------------------------------------- */
    
    function togglePart1Submenu(expand) {
        if (!part1SubmenuContainer) return;
        if (expand) {
            part1SubmenuContainer.style.display = "block";
            if (part1ExpandIcon) part1ExpandIcon.innerHTML = `<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m18 15-6-6-6 6"/></svg>`;
        } else {
            part1SubmenuContainer.style.display = "none";
            if (part1ExpandIcon) part1ExpandIcon.innerHTML = `<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>`;
        }
    }
    function togglePart2Submenu(expand) {
        if (!part2SubmenuContainer) return;
        if (expand) {
            part2SubmenuContainer.style.display = "block";
            if (part2ExpandIcon) part2ExpandIcon.innerHTML = `<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m18 15-6-6-6 6"/></svg>`;
        } else {
            part2SubmenuContainer.style.display = "none";
            if (part2ExpandIcon) part2ExpandIcon.innerHTML = `<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>`;
        }
    }

    function togglePart3Submenu(expand) {
        if (expand) {
            part3SubmenuContainer.style.display = "block";
            part3ExpandIcon.innerHTML = icons.chevronUp;
        } else {
            part3SubmenuContainer.style.display = "none";
            part3ExpandIcon.innerHTML = icons.chevronDown;
        }
    }

    function togglePart4Submenu(expand) {
        if (expand) {
            part4SubmenuContainer.style.display = "block";
            part4ExpandIcon.innerHTML = icons.chevronUp;
        } else {
            part4SubmenuContainer.style.display = "none";
            part4ExpandIcon.innerHTML = icons.chevronDown;
        }
    }

    function switchView(viewName) {
        if (!window.isUnlocked && (viewName === "part2" || viewName === "part3" || viewName === "part4")) {
            window.showPaywallModal(() => switchView(viewName));
            return;
        }
        state.activeView = viewName;
        stopAudio();
        
        // Update sidebar highlights
        if (viewName === "home") {
            navHomeBtn.classList.add("active");
            navPart2Btn.classList.remove("active");
            navPart3Btn.classList.remove("active");
            navPart4Btn.classList.remove("active");
            document.querySelectorAll(".submenu-item").forEach(item => item.classList.remove("active"));
            if (typeof togglePart1Submenu !== "undefined") togglePart1Submenu(false);
            togglePart3Submenu(false);
            togglePart4Submenu(false);
        } else if (viewName === "part2") {
            navHomeBtn.classList.remove("active");
            navPart2Btn.classList.add("active");
            navPart3Btn.classList.remove("active");
            if (navPart4Btn) navPart4Btn.classList.remove("active");
            document.querySelectorAll(".submenu-item").forEach(item => item.classList.remove("active"));
            
            if (typeof togglePart1Submenu !== "undefined") togglePart1Submenu(false);
            if (typeof togglePart2Submenu !== "undefined") togglePart2Submenu(true);
            togglePart3Submenu(false);
            togglePart4Submenu(false);
            
            if (state.part02ActiveSection) {
                loadSectionP2(state.part02ActiveSection);
            } else {
                if (typeof categoryTreeP2 !== "undefined" && categoryTreeP2.length > 0) {
                    loadSectionP2(categoryTreeP2[0].id);
                }
            }
        
        } else if (viewName === "part1") {
            navHomeBtn.classList.remove("active");
            navPart2Btn.classList.remove("active");
            navPart3Btn.classList.remove("active");
            if (navPart4Btn) navPart4Btn.classList.remove("active");
            if (navPart1Btn) navPart1Btn.classList.add("active");
            
            document.querySelectorAll(".submenu-item").forEach(item => {
                if (item.getAttribute("data-id") === state.part01ActiveSection) {
                    item.classList.add("active");
                } else {
                    item.classList.remove("active");
                }
            });
            if (typeof togglePart3Submenu !== 'undefined') togglePart3Submenu(false);
            if (typeof togglePart4Submenu !== 'undefined') togglePart4Submenu(false);
            togglePart1Submenu(true);
            
            if (!state.part01ActiveSection || state.part01ActiveSection === "overview") {
                loadSectionP1("overview");
            } else {
                loadSectionP1(state.part01ActiveSection);
            }
        } else if (viewName === "part3") {
            navHomeBtn.classList.remove("active");
            navPart2Btn.classList.remove("active");
            navPart3Btn.classList.add("active");
            document.querySelectorAll(".submenu-item").forEach(item => {
                if (item.getAttribute("data-id") === state.part03ActiveSection) {
                    item.classList.add("active");
                } else {
                    item.classList.remove("active");
                }
            });
            if (typeof togglePart1Submenu !== "undefined") togglePart1Submenu(false);
            togglePart3Submenu(true);
            togglePart4Submenu(false);
        } else if (viewName === "part4") {
            navHomeBtn.classList.remove("active");
            navPart2Btn.classList.remove("active");
            navPart3Btn.classList.remove("active");
            navPart4Btn.classList.add("active");
            document.querySelectorAll(".submenu-item").forEach(item => {
                if (item.getAttribute("data-id") === state.part04ActiveSection) {
                    item.classList.add("active");
                } else {
                    item.classList.remove("active");
                }
            });
            togglePart3Submenu(false);
            if (typeof togglePart1Submenu !== "undefined") togglePart1Submenu(false);
            togglePart4Submenu(true);
            if (!state.part04ActiveSection || state.part04ActiveSection === "overview") {
                loadSectionP4("overview");
            } else {
                loadSectionP4(state.part04ActiveSection);
            }
        }
        
        // Toggle views
        contentViews.forEach(view => {
            if (view.id === `view-${viewName}`) {
                view.classList.add("active");
            } else {
                view.classList.remove("active");
            }
        });
        
        // Sync Main Title Header
        if (viewName === "home") {
            mainTitleText.textContent = "TOEIC LISTENING ZONE";
        } else if (viewName === "part2") {
            mainTitleText.textContent = "PART 02: QUESTIONS-RESPONSES";
        
        } else if (viewName === "part1") {
            navHomeBtn.classList.remove("active");
            navPart2Btn.classList.remove("active");
            navPart3Btn.classList.remove("active");
            if (navPart4Btn) navPart4Btn.classList.remove("active");
            if (navPart1Btn) navPart1Btn.classList.add("active");
            
            document.querySelectorAll(".submenu-item").forEach(item => {
                if (item.getAttribute("data-id") === state.part01ActiveSection) {
                    item.classList.add("active");
                } else {
                    item.classList.remove("active");
                }
            });
            if (typeof togglePart3Submenu !== 'undefined') togglePart3Submenu(false);
            if (typeof togglePart4Submenu !== 'undefined') togglePart4Submenu(false);
            togglePart1Submenu(true);
            
            if (!state.part01ActiveSection || state.part01ActiveSection === "overview") {
                loadSectionP1("overview");
            } else {
                loadSectionP1(state.part01ActiveSection);
            }
        } else if (viewName === "part3") {
            mainTitleText.textContent = "PART 03: SHORT CONVERSATIONS";
        } else if (viewName === "part4") {
            mainTitleText.textContent = "PART 04: SHORT TALKS";
        }
    }
    
    navHomeBtn.addEventListener("click", () => switchView("home"));
    
    if (navPart1Btn) {
        navPart1Btn.addEventListener("click", () => {
            if (state.activeView === "part1") {
                const isVisible = part1SubmenuContainer.style.display === "block";
                togglePart1Submenu(!isVisible);
            } else {
                switchView("part1");
            }
        });
    }

    navPart2Btn.addEventListener("click", () => {
        if (viewPart2.classList.contains("active")) {
            const isExpanded = part2SubmenuContainer.style.display === "block";
            togglePart2Submenu(!isExpanded);
        } else {
            switchView("part2");
        }
    });
    
    navPart3Btn.addEventListener("click", () => {
        if (!window.isUnlocked) {
            window.showPaywallModal(() => {
                if (state.activeView !== "part3") {
                    loadSection(state.part03ActiveSection || "overview");
                }
            });
            return;
        }
        if (state.activeView === "part3") {
            const isVisible = part3SubmenuContainer.style.display === "block";
            togglePart3Submenu(!isVisible);
        } else {
            loadSection(state.part03ActiveSection || "overview");
        }
    });

    if (typeof navPart4Btn !== 'undefined' && navPart4Btn) {
        navPart4Btn.addEventListener("click", () => {
            if (!window.isUnlocked) {
                window.showPaywallModal(() => {
                    if (state.activeView !== "part4") {
                        loadSectionP4(state.part04ActiveSection || "overview");
                    }
                });
                return;
            }
            if (state.activeView === "part4") {
                const isVisible = part4SubmenuContainer.style.display === "block";
                togglePart4Submenu(!isVisible);
            } else {
                loadSectionP4(state.part04ActiveSection || "overview");
            }
        });
    }
    
    // Quick triggers from Dashboard
    const cardPart1 = document.getElementById("card-part1");
    if (cardPart1) {
        cardPart1.addEventListener("click", () => switchView("part1"));
    }
    
    const cardPart2 = document.getElementById("card-part2");
    if (cardPart2) {
        cardPart2.addEventListener("click", () => switchView("part2"));
    }
    const cardPart3 = document.getElementById("card-part3");
    if (cardPart3) {
        cardPart3.addEventListener("click", () => loadSection("overview"));
    }
    const cardPart4 = document.getElementById("card-part4");
    if (cardPart4) {
        cardPart4.addEventListener("click", () => loadSectionP4("overview"));
    }


    // Sidebar Toggling
    toggleSidebarBtn.addEventListener("click", () => {
        sidebar.classList.toggle("collapsed");
        if (sidebar.classList.contains("collapsed")) {
            toggleIcon.innerHTML = `<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m13 17 5-5-5-5M6 17l5-5-5-5"/></svg>`;
        } else {
            toggleIcon.innerHTML = `<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m11 17-5-5 5-5M18 17l-5-5 5-5"/></svg>`;
        }
    });

    /* -------------------------------------------------------------
       4. AUDIO PLAYER
       ------------------------------------------------------------- */
    function stopAudio() {
        if (state.currentAudio) {
            state.currentAudio.pause();
            state.currentAudio = null;
        }
        if (state.currentAudioBtn) {
            state.currentAudioBtn.innerHTML = icons.play;
            state.currentAudioBtn = null;
        }
    }

    function createAudioPlayer(audioFile, container) {
        if (!audioFile) {
            container.innerHTML = `
                <div class="audio-player-card">
                    <p style="color: var(--text-muted); font-size: 0.85rem; text-align: center; font-weight: 700; margin: 0;">
                        🔇 Không có file âm thanh nghe.
                    </p>
                </div>
            `;
            return;
        }
        
        const audioUrl = `media/${audioFile}`;
        
        container.innerHTML = `
            <div class="audio-player-card" style="border-bottom: 1px solid var(--border); background: rgba(255,255,255,0.015);">
                <div class="audio-controls-row">
                    <button class="play-pause-btn" id="play-pause-control">
                        ${icons.play}
                    </button>
                    
                    <div class="progress-bar-wrapper">
                        <span class="time-stamp" id="time-current">00:00</span>
                        <input type="range" class="progress-slider" id="progress-slider" min="0" value="0" step="0.1">
                        <span class="time-stamp" id="time-duration">00:00</span>
                    </div>
                    
                    <div class="speed-selector-wrapper">
                        <select class="speed-select" id="speed-select">
                            <option value="0.75">0.75x</option>
                            <option value="1.0" selected>1.0x (Chuẩn)</option>
                            <option value="1.2">1.2x</option>
                            <option value="1.5">1.5x</option>
                        </select>
                    </div>
                </div>
            </div>
        `;
        
        const playBtn = container.querySelector("#play-pause-control");
        const slider = container.querySelector("#progress-slider");
        const timeCurrent = container.querySelector("#time-current");
        const timeDuration = container.querySelector("#time-duration");
        const speedSelect = container.querySelector("#speed-select");
        
        const audio = new Audio(audioUrl);
        
        const formatTime = (secs) => {
            const m = Math.floor(secs / 60).toString().padStart(2, "0");
            const s = Math.floor(secs % 60).toString().padStart(2, "0");
            return `${m}:${s}`;
        };
        
        audio.addEventListener("loadedmetadata", () => {
            slider.max = audio.duration;
            timeDuration.textContent = formatTime(audio.duration);
        });
        
        audio.addEventListener("timeupdate", () => {
            if (!slider.dragging) {
                slider.value = audio.currentTime;
                timeCurrent.textContent = formatTime(audio.currentTime);
            }
        });
        
        audio.addEventListener("ended", () => {
            playBtn.innerHTML = icons.play;
        });
        
        playBtn.addEventListener("click", () => {
            if (audio.paused) {
                stopAudio();
                
                audio.playbackRate = parseFloat(speedSelect.value);
                audio.play();
                playBtn.innerHTML = icons.pause;
                
                state.currentAudio = audio;
                state.currentAudioBtn = playBtn;
            } else {
                audio.pause();
                playBtn.innerHTML = icons.play;
                state.currentAudio = null;
                state.currentAudioBtn = null;
            }
        });
        
        slider.addEventListener("mousedown", () => slider.dragging = true);
        slider.addEventListener("mouseup", () => {
            slider.dragging = false;
            audio.currentTime = slider.value;
        });
        slider.addEventListener("change", () => {
            audio.currentTime = slider.value;
        });
        
        speedSelect.addEventListener("change", () => {
            audio.playbackRate = parseFloat(speedSelect.value);
        });
    }

    /* -------------------------------------------------------------
       5. DATA PREPROCESSING & DYNAMIC SIDEBAR
       ------------------------------------------------------------- */
    function cleanQuestionText(qText) {
        if (!qText) return "";
        let clean = qText.trim();
        clean = clean.replace(/<strong[^>]*>\s*(Example|EXAMPLE)\s*\d+\s*(:\s*)?<\/strong>/gi, "");
        clean = clean.replace(/<strong[^>]*>\s*<span[^>]*>\s*(Example|EXAMPLE)\s*\d+\s*<\/span>\s*<\/strong>/gi, "");
        clean = clean.replace(/<strong[^>]*>\s*Question:\s*<\/strong>/gi, "");
        clean = clean.replace(/^(Example|EXAMPLE)\s*\d+(\s*:\s*)?/gi, "");
        clean = clean.replace(/^Question\s*:\s*/gi, "");
        clean = clean.replace(/^(<br\s*\/?>|&nbsp;|\s)+/gi, "");
        clean = clean.replace(/(<br\s*\/?>|&nbsp;|\s)+$/gi, "");
        clean = clean.replace(/^<strong[^>]*>\s*<\/strong>/gi, "");
        clean = clean.replace(/^<em[^>]*>\s*<\/em>/gi, "");
        clean = clean.replace(/^(<br\s*\/?>|&nbsp;|\s)+/gi, "").trim();
        return clean;
    }

    function normalizeChoices(choicesObj) {
        let parts = [];
        const keys = Object.keys(choicesObj).sort();
        
        keys.forEach(k => {
            let val = choicesObj[k].trim();
            let cleanVal = val.replace(/<[^>]+>/g, "").replace(/&nbsp;/g, " ").trim();
            let labelRegex = new RegExp("^" + k + "\\s*\\.\\s*", "i");
            if (!labelRegex.test(cleanVal)) {
                parts.push(k + ". " + cleanVal);
            } else {
                let textWithoutLabel = cleanVal.replace(labelRegex, "").trim();
                parts.push(k + ". " + textWithoutLabel);
            }
        });
        
        let combined = "\t" + parts.join("\t");
        let aMatch = combined.match(/(?<=\t)A\s*\.\s*([\s\S]*?)(?=\tB\s*\.\s*|$)/i);
        let bMatch = combined.match(/(?<=\t)B\s*\.\s*([\s\S]*?)(?=\tC\s*\.\s*|$)/i);
        let cMatch = combined.match(/(?<=\t)C\s*\.\s*([\s\S]*?)(?=\tD\s*\.\s*|$)/i);
        let dMatch = combined.match(/(?<=\t)D\s*\.\s*([\s\S]*?)$/i);
        
        let result = {
            'A': aMatch ? aMatch[1].trim() : "",
            'B': bMatch ? bMatch[1].trim() : "",
            'C': cMatch ? cMatch[1].trim() : "",
            'D': dMatch ? dMatch[1].trim() : ""
        };
        
        Object.keys(result).forEach(k => {
            let text = result[k];
            text = text.replace(/\s+/g, " ").trim();
            text = text.replace(/&amp;/g, "&").replace(/&quot;/g, '"');
            result[k] = text;
        });
        
        return result;
    }

    if (window.part03Data) {
        state.part03Data = window.part03Data;
        
        state.part03Data.forEach(item => {
            if (item.examples && item.examples.length > 0) {
                item.examples.forEach(ex => {
                    if (ex.questions) {
                        // It is an example set for topics
                        ex.questions.forEach(eq => {
                            eq.question = cleanQuestionText(eq.question);
                            if (eq.choices) eq.choices = normalizeChoices(eq.choices);
                        });
                    } else {
                        // It is a single example for subsections
                        ex.question = cleanQuestionText(ex.question);
                        if (ex.choices) {
                            ex.choices = normalizeChoices(ex.choices);
                        }
                    }
                });
            }

            if (item.practice && item.practice.length > 0) {
                item.practice.forEach(q => {
                    q.question = cleanQuestionText(q.question);
                    if (q.choices) {
                        q.choices = normalizeChoices(q.choices);
                    }
                });
            }
        });

        initializePart03Sidebar();
        updateRouteProgress();
    }

    function initializePart03Sidebar() {
        conceptsNavList.innerHTML = "";
        topicsNavList.innerHTML = "";
        
        const isUnlocked = window.isUnlocked;
        
        // Render Dạng câu hỏi (concepts) using the category tree
        categoryTree.forEach(node => {
            if (node.type === "item") {
                const submenuItem = document.createElement("div");
                submenuItem.className = "submenu-item";
                submenuItem.setAttribute("data-id", node.id);
                
                let text = node.title.toUpperCase();
                if (LOCKED_SECTIONS.includes(node.id) && !isUnlocked) {
                    text += " 🔒";
                }
                submenuItem.textContent = text;
                
                submenuItem.addEventListener("click", (e) => {
                    e.stopPropagation();
                    loadSection(node.id);
                });
                conceptsNavList.appendChild(submenuItem);
            } else if (node.type === "group") {
                // Render group header
                const groupHeader = document.createElement("div");
                groupHeader.className = "sidebar-group-header";
                groupHeader.textContent = node.title.toUpperCase();
                conceptsNavList.appendChild(groupHeader);
                
                // Render items inside group
                node.items.forEach(item => {
                    const submenuItem = document.createElement("div");
                    submenuItem.className = "submenu-item group-item";
                    submenuItem.setAttribute("data-id", item.id);
                    
                    let text = item.title.toUpperCase();
                    if (LOCKED_SECTIONS.includes(item.id) && !isUnlocked) {
                        text += " 🔒";
                    }
                    submenuItem.textContent = text;
                    
                    submenuItem.addEventListener("click", (e) => {
                        e.stopPropagation();
                        loadSection(item.id);
                    });
                    conceptsNavList.appendChild(submenuItem);
                });
            }
        });
        
        // Render Chủ đề nghe (topics)
        state.part03Data.forEach(item => {
            if (item.type === "topic" || item.type === "test") {
                const submenuItem = document.createElement("div");
                submenuItem.className = "submenu-item";
                submenuItem.setAttribute("data-id", item.id);
                
                let text = item.title.toUpperCase();
                if (LOCKED_SECTIONS.includes(item.id) && !isUnlocked) {
                    text += " 🔒";
                }
                submenuItem.textContent = text;
                
                submenuItem.addEventListener("click", (e) => {
                    e.stopPropagation();
                    loadSection(item.id);
                });
                
                topicsNavList.appendChild(submenuItem);
            }
        });
    }


    if (window.part04Data) {
        state.part04Data = window.part04Data;
        
        state.part04Data.forEach(item => {
            if (item.examples && item.examples.length > 0) {
                item.examples.forEach(ex => {
                    if (ex.questions) {
                        // It is an example set for topics
                        ex.questions.forEach(eq => {
                            eq.question = cleanQuestionText(eq.question);
                            if (eq.choices) eq.choices = normalizeChoices(eq.choices);
                        });
                    } else {
                        // It is a single example for subsections
                        ex.question = cleanQuestionText(ex.question);
                        if (ex.choices) {
                            ex.choices = normalizeChoices(ex.choices);
                        }
                    }
                });
            }

            if (item.practice && item.practice.length > 0) {
                item.practice.forEach(q => {
                    q.question = cleanQuestionText(q.question);
                    if (q.choices) {
                        q.choices = normalizeChoices(q.choices);
                    }
                });
            }
        });

        initializePart01Sidebar();
        initializePart02Sidebar();
        initializePart04Sidebar();
        updateRouteProgress();
    }

    
    function initializePart01Sidebar() {
        if (!part1ConceptsNavList || !part1TopicsNavList) return;
        
        part1ConceptsNavList.innerHTML = "";
        part1TopicsNavList.innerHTML = "";
        
        const isUnlocked = window.isUnlocked;
        
        categoryTreeP1.forEach(node => {
            if (node.type === "item") {
                const submenuItem = document.createElement("div");
                submenuItem.className = "submenu-item";
                submenuItem.setAttribute("data-id", node.id);
                
                let text = node.title.toUpperCase();
                if (LOCKED_SECTIONS.includes(node.id) && !isUnlocked) {
                    text += " 🔒";
                }
                
                submenuItem.innerHTML = `<span class="submenu-dot"></span><span class="submenu-text">${text}</span>`;
                
                submenuItem.addEventListener("click", (e) => {
                    e.stopPropagation();
                    if (LOCKED_SECTIONS.includes(node.id) && !window.isUnlocked) {
                        window.showPaywallModal(() => loadSectionP1(node.id));
                        return;
                    }
                    loadSectionP1(node.id);
                });
                
                part1ConceptsNavList.appendChild(submenuItem);
            }
        });
        
        // Render Tests for Part 1
        if (window.part01Data) {
            window.part01Data.forEach(section => {
                if (section.type === "test") {
                    const submenuItem = document.createElement("div");
                    submenuItem.className = "submenu-item";
                    submenuItem.setAttribute("data-id", section.id);
                    
                    let text = section.title.toUpperCase();
                    if (LOCKED_SECTIONS.includes(section.id) && !isUnlocked) {
                        text += " 🔒";
                    }
                    
                    submenuItem.innerHTML = `<span class="submenu-dot"></span><span class="submenu-text">${text}</span>`;
                    
                    submenuItem.addEventListener("click", (e) => {
                        e.stopPropagation();
                        if (LOCKED_SECTIONS.includes(section.id) && !window.isUnlocked) {
                            window.showPaywallModal(() => loadSectionP1(section.id));
                            return;
                        }
                        loadSectionP1(section.id);
                    });
                    
                    part1TopicsNavList.appendChild(submenuItem);
                }
            });
        }
    }

    function initializePart04Sidebar() {
        if (!part4ConceptsNavList || !part4TopicsNavList) return;
        
        part4ConceptsNavList.innerHTML = "";
        part4TopicsNavList.innerHTML = "";
        
        const isUnlocked = window.isUnlocked;
        
        // Render Dạng câu hỏi (concepts) using the category tree P4
        categoryTreeP4.forEach(node => {
            if (node.type === "item") {
                const submenuItem = document.createElement("div");
                submenuItem.className = "submenu-item";
                submenuItem.setAttribute("data-id", node.id);
                
                let text = node.title.toUpperCase();
                if (LOCKED_SECTIONS.includes(node.id) && !isUnlocked) {
                    text += " 🔒";
                }
                submenuItem.textContent = text;
                
                submenuItem.addEventListener("click", (e) => {
                    e.stopPropagation();
                    loadSectionP4(node.id);
                });
                part4ConceptsNavList.appendChild(submenuItem);
            } else if (node.type === "group") {
                // Render group header
                const groupHeader = document.createElement("div");
                groupHeader.className = "sidebar-group-header";
                groupHeader.textContent = node.title.toUpperCase();
                part4ConceptsNavList.appendChild(groupHeader);
                
                // Render items inside group
                node.items.forEach(item => {
                    const submenuItem = document.createElement("div");
                    submenuItem.className = "submenu-item group-item";
                    submenuItem.setAttribute("data-id", item.id);
                    
                    let text = item.title.toUpperCase();
                    if (LOCKED_SECTIONS.includes(item.id) && !isUnlocked) {
                        text += " 🔒";
                    }
                    submenuItem.textContent = text;
                    
                    submenuItem.addEventListener("click", (e) => {
                        e.stopPropagation();
                        loadSectionP4(item.id);
                    });
                    part4ConceptsNavList.appendChild(submenuItem);
                });
            }
        });
        
        // Render Bài Test ETS (topics)
        state.part04Data.forEach(item => {
            if (item.type === "test") {
                const submenuItem = document.createElement("div");
                submenuItem.className = "submenu-item";
                submenuItem.setAttribute("data-id", item.id);
                
                let text = item.title.toUpperCase();
                if (LOCKED_SECTIONS.includes(item.id) && !isUnlocked) {
                    text += " 🔒";
                }
                submenuItem.textContent = text;
                
                submenuItem.addEventListener("click", (e) => {
                    e.stopPropagation();
                    loadSectionP4(item.id);
                });
                
                part4TopicsNavList.appendChild(submenuItem);
            }
        });
    }

    function loadSection(id) {
        const isUnlocked = window.isUnlocked;
        if (LOCKED_SECTIONS.includes(id) && !isUnlocked) {
            window.showPaywallModal(() => loadSection(id));
            return;
            if (false) {
                sessionStorage.setItem("portal_unlocked_v2", "true");
                alert("Mở khóa thành công!");
                initializePart03Sidebar();
    initializePart01Sidebar();
    if (typeof initializePart02Sidebar === 'function') initializePart02Sidebar();
    initializePart04Sidebar(); // Refresh sidebar to remove locks
            } else {
                if (pass !== null) {
                    alert("Mật khẩu không chính xác!");
                }
                // Fallback to active section or overview
                const fallbackId = state.part03ActiveSection && state.part03ActiveSection !== id ? state.part03ActiveSection : "overview";
                document.querySelectorAll(".submenu-item").forEach(item => {
                    if (item.getAttribute("data-id") === fallbackId) {
                        item.classList.add("active");
                    } else {
                        item.classList.remove("active");
                    }
                });
                return;
            }
        }
        
        state.part03ActiveSection = id;
        
        if (state.activeView !== "part3") {
            switchView("part3");
        }
        
        document.querySelectorAll(".submenu-item").forEach(item => {
            if (item.getAttribute("data-id") === id) {
                item.classList.add("active");
            } else {
                item.classList.remove("active");
            }
        });
        
        const isGeneral = id === "overview" || id === "tips";
        const panelSectionsBar = document.getElementById("panel-sections-bar");
        if (panelSectionsBar) {
            panelSectionsBar.style.display = isGeneral ? "none" : "flex";
        }
        
        const section = state.part03Data.find(item => item.id === id);
        if (!section) return;
        
        // Override section title using category tree mapping
        let displayTitle = section.title;
        let parentText = "Lý thuyết chung";
        
        let foundNode = null;
        categoryTree.forEach(node => {
            if (node.type === "item" && node.id === id) {
                foundNode = node;
                parentText = "Tổng quan";
            } else if (node.type === "group") {
                const match = node.items.find(item => item.id === id);
                if (match) {
                    foundNode = match;
                    parentText = node.title;
                }
            }
        });
        
        if (foundNode) {
            displayTitle = foundNode.title;
        } else if (section.type === "topic" || section.type === "test") {
            parentText = "Luyện tập ETS 2026";
            displayTitle = section.title;
        }
        
        breadParent.textContent = parentText;
        breadCurrent.textContent = displayTitle;
        panelTitle.textContent = displayTitle;
        
        const hasTheory = section.theory && section.theory.length > 0;
        const theoryTabBtn = document.getElementById("sec-btn-theory");
        if (theoryTabBtn) {
            if (hasTheory) {
                theoryTabBtn.classList.remove("hidden");
            } else {
                theoryTabBtn.classList.add("hidden");
            }
        }

        const hasVocabulary = section.vocabulary && section.vocabulary.length > 0;
        const vocabularyTabBtn = document.getElementById("sec-btn-vocabulary");
        if (vocabularyTabBtn) {
            if (hasVocabulary) {
                vocabularyTabBtn.classList.remove("hidden");
            } else {
                vocabularyTabBtn.classList.add("hidden");
            }
        }

        const hasExamples = section.examples && section.examples.length > 0;
        const examplesTabBtn = document.getElementById("sec-btn-examples");
        if (examplesTabBtn) {
            if (hasExamples) {
                examplesTabBtn.classList.remove("hidden");
            } else {
                examplesTabBtn.classList.add("hidden");
            }
        }

        const hasPractice = (section.practice && section.practice.length > 0) || (section.practice_sets && section.practice_sets.length > 0);
        const practiceTabBtn = document.getElementById("sec-btn-practice");
        if (practiceTabBtn) {
            if (hasPractice) {
                practiceTabBtn.classList.remove("hidden");
            } else {
                practiceTabBtn.classList.add("hidden");
            }
        }

        // Auto-switch to the first tab that has content
        let targetTab = "theory";
        if (section.theory && section.theory.length > 0) {
            targetTab = "theory";
        } else if (section.vocabulary && section.vocabulary.length > 0) {
            targetTab = "vocabulary";
        } else if (section.examples && section.examples.length > 0) {
            targetTab = "examples";
        } else if ((section.practice && section.practice.length > 0) || (section.practice_sets && section.practice_sets.length > 0)) {
            targetTab = "practice";
        }
        state.part03ActiveTab = targetTab;
        
        renderPanelTab(state.part03ActiveTab);
    }
    
    panelTabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            const sec = btn.getAttribute("data-section");
            state.part03ActiveTab = sec;
            renderPanelTab(sec);
        });
    });

    function renderPanelTab(tabName) {
        stopAudio();
        
        panelTabs.forEach(tab => {
            if (tab.id === `sec-${tabName}`) {
                tab.classList.add("active");
            } else {
                tab.classList.remove("active");
            }
        });
        
        panelTabBtns.forEach(b => {
            if (b.getAttribute("data-section") === tabName) {
                b.classList.add("active");
            } else {
                b.classList.remove("active");
            }
        });
        
        const section = state.part03Data.find(item => item.id === state.part03ActiveSection);
        if (!section) return;
        
        if (tabName === "theory") {
            renderTheory(section);
        } else if (tabName === "vocabulary") {
            renderVocabulary(section);
        } else if (tabName === "examples") {
            renderExamples(section);
        } else if (tabName === "practice") {
            renderPractice(section);
        }
    }

    /* -------------------------------------------------------------
       5.5 TRANSLATION HTML BUILDERS
       ------------------------------------------------------------- */
    function renderQuestionTextHtml(q, idLabel, textPrefix = "") {
        let qText = q.question;
        if (qText) {
            qText = qText.replace(/^(?:<[^>]*>)?\s*Question\s*\d+[\.\:]\s*(?:<\/[^>]*>)?\s*/i, "");
            if (qText.includes("PRACTICE") || qText.includes("Example") || qText.includes("EXAMPLE")) {
                textPrefix = "";
            }
        }
        const qViet = q.vietnamese_question || "";
        
        let graphicHtml = "";
        const lowerQText = (qText || "").toLowerCase();
        const lowerQViet = (qViet || "").toLowerCase();
        const isVisual = lowerQText.includes("look at the graphic") || 
                         lowerQText.includes("look at the map") ||
                         lowerQText.includes("look at the schedule") ||
                         lowerQText.includes("look at the chart") ||
                         lowerQText.includes("look at the diagram") ||
                         lowerQViet.includes("quan sát hình") ||
                         lowerQViet.includes("nhìn vào hình") ||
                         lowerQViet.includes("quan sát sơ đồ") ||
                         lowerQViet.includes("nhìn vào sơ đồ");
                         
        if (isVisual) {
            const CROPPED_GRAPHICS = {
                327: "data/graphics/Slide327.png",
                336: "data/graphics/Slide336.png",
                436: "data/graphics/Slide436.png",
                441: "data/graphics/Slide441.png",
                455: "data/graphics/Slide455.png",
                481: "data/graphics/Slide481.png",
                490: "data/graphics/Slide490.png",
                540: "data/graphics/Slide540.png"
            };
            let imgSrc = `../TOECI LISTENING - PART 03/Slide${q.slide_index}.png`;
            if (CROPPED_GRAPHICS[q.slide_index]) {
                imgSrc = CROPPED_GRAPHICS[q.slide_index];
            }
            graphicHtml = `
                <div class="visual-graphic-container" style="margin: 16px 0; text-align: center; width: 100%;">
                    <img class="visual-graphic-img" 
                         src="${imgSrc}" 
                         onerror="this.onerror=null; this.src='../TOEIC LISTENING - PART 03/Slide${q.slide_index}.png';"
                         style="max-width: 100%; max-height: 450px; border: 2px solid var(--border); border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); display: block; margin: 0 auto;" 
                         alt="Look at the graphic (Slide ${q.slide_index})">
                </div>
            `;
        }

        if (!qViet) {
            return `
                <div class="question-text" style="font-size: 1.25rem; font-weight: 700; line-height: 1.5; color: var(--text-main); margin-bottom: 16px;">${textPrefix}${qText}</div>
                ${graphicHtml}
            `;
        }
        
        return `
            <div class="question-text-wrapper" style="cursor: pointer; width: 100%;" onclick="const t = this.querySelector('.q-trans'); t.style.display = t.style.display === 'block' ? 'none' : 'block'; event.stopPropagation();" title="Click vào câu hỏi để xem dịch nghĩa">
                <div class="question-text" style="margin-bottom: 16px; text-align: left; width: 100%; font-size: 1.25rem; font-weight: 700; line-height: 1.5; color: var(--text-main);">
                    ${textPrefix}${qText}
                </div>
                <div class="q-trans" style="display: none;">
                    ${qViet}
                </div>
            </div>
            ${graphicHtml}
        `;
    }

    function renderChoicesHtml(q, isReview = false, userAnswer = null) {
        let choicesHtml = "";
        Object.keys(q.choices).forEach(key => {
            const optText = q.choices[key];
            const optViet = q.vietnamese_choices ? q.vietnamese_choices[key] : "";
            
            let extraClass = "";
            if (isReview) {
                extraClass = "checked-done";
                if (key === q.answer) {
                    extraClass += " correct";
                } else if (key === userAnswer) {
                    extraClass += " incorrect";
                }
            }
            
            let transDiv = "";
            if (optViet) {
                transDiv = `
                    <div class="c-trans" style="display: none; color: var(--color-purple); font-size: 0.88rem; font-style: italic; margin-top: 6px; text-align: left; width: 100%; border-left: 2px solid var(--color-purple); padding-left: 8px; line-height: 1.4; font-weight: 500;">
                        ${optViet}
                    </div>
                `;
            }
            
            choicesHtml += `
                <button class="choice-option ${extraClass}" data-key="${key}" data-slide="${q.slide_index}" data-q-slide="${q.slide_index}" style="display: flex; flex-direction: column; align-items: flex-start; padding: 12px 16px; width: 100%; border-radius: 0px !important;">
                    <div style="display: flex; align-items: center; width: 100%;">
                        <div class="choice-radio-circle"></div>
                        <div class="choice-letter" style="margin-right: 12px; flex-shrink: 0;">${key}</div>
                        <div class="choice-text" style="flex: 1; text-align: left; font-weight: 500; padding-right: 8px;">${optText}</div>
                    </div>
                    ${transDiv}
                </button>
            `;
        });
        return choicesHtml;
    }

    function renderTranscriptHtml(transcriptList, vietTranscriptList) {
        let html = "";
        transcriptList.forEach((line, idx) => {
            const lineViet = vietTranscriptList && vietTranscriptList[idx] ? vietTranscriptList[idx] : "";
            let transHtml = "";
            if (lineViet) {
                const cleanViet = lineViet.replace(/^[A-Za-z0-9]+[-A-Za-z0-9]*\s*:\s*/, "");
                const highlightedViet = cleanViet.replace(/(\(\d+\)[^.?!]*(?:[.?!]|$))/g, '<strong style="color: #ff3333; font-style: italic;">$1</strong>');
                transHtml = `<div class="line-trans-text" style="color: var(--text-muted); font-size: 0.88rem; font-style: italic; margin-top: 4px; border-left: 2px solid var(--border); padding-left: 8px;">${highlightedViet}</div>`;
            }
            let formattedLine = line.replace(/(\(\d+\)[^.?!]*(?:[.?!]|$))/g, '<strong style="color: #ff3333; font-style: italic;">$1</strong>');
            formattedLine = formattedLine.replace(/^([A-Za-z0-9]+[-A-Za-z0-9]*\s*:\s*)/, '<strong style="color: var(--color-blue);">$1</strong>');
            html += `
                <div class="transcript-line-wrapper" style="margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px dashed var(--border); text-align: left;">
                    <p class="transcript-line" style="margin: 0; font-weight: 500; line-height: 1.5;">${formattedLine}</p>
                    ${transHtml}
                </div>
            `;
        });
        return html;
    }

    function renderScriptCardHtml(idLabel, transcriptHtml, explanationHtml) {
        return `
            <div class="reveal-script-card hidden" id="reveal-card-${idLabel}">
                <div class="reveal-header" id="header-reveal-${idLabel}">
                    <span><strong>📄 TRANSCRIPT & GIẢI THÍCH ĐÁP ÁN</strong></span>
                    ${icons.chevronDown}
                </div>
                <div class="reveal-content" id="reveal-content-${idLabel}" style="padding: 20px; text-align: left;">
                    ${explanationHtml}
                    <h4 style="margin: 20px 0 10px 0; font-size: 1rem; font-weight: 800; text-transform: uppercase; color: var(--color-purple); display: flex; align-items: center; gap: 8px; border-bottom: 1px solid var(--border); padding-bottom: 8px;">
                        🎤 TRANSCRIPT BÀI NGHE
                    </h4>
                    ${transcriptHtml}
                </div>
            </div>
        `;
    }

    function hookScriptCardToggler(idLabel) {
        setTimeout(() => {
            const revHeader = document.getElementById(`header-reveal-${idLabel}`);
            const revContent = document.getElementById(`reveal-content-${idLabel}`);
            if (revHeader && revContent) {
                revHeader.addEventListener("click", () => {
                    revContent.classList.toggle("open");
                    const svg = revHeader.querySelector("svg");
                    if (svg) {
                        if (revContent.classList.contains("open")) {
                            svg.outerHTML = icons.chevronUp;
                        } else {
                            svg.outerHTML = icons.chevronDown;
                        }
                    }
                });
            }
        }, 50);
    }

    /* -------------------------------------------------------------
       6. RENDERING DETAILS (THEORY, VOCABULARY, EXAMPLES, PRACTICE)
       ------------------------------------------------------------- */
    
    // A. THEORY
    function renderTheory(section) {
        theoryContentArea.innerHTML = "";
        
        if (!section.theory || section.theory.length === 0) {
            theoryContentArea.innerHTML = "<p style='color: var(--text-muted); font-weight: 700;'>Không có lý thuyết cho phần này.</p>";
            return;
        }
        
        // Custom interactive landing page for Section Overview (Inspired by Speaking website design elements)
        if (section.id === "overview") {
            theoryContentArea.innerHTML = `
                <style>
                    .overview-hero-p3 {
                        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #4338ca 100%);
                        color: white; padding: 45px 40px; border-radius: 20px; position: relative; overflow: hidden;
                        box-shadow: 0 20px 40px rgba(0,0,0,0.25); margin-bottom: 40px; border: 1px solid rgba(255, 255, 255, 0.1);
                    }
                    .overview-hero-p3::before {
                        content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
                        background: radial-gradient(circle, rgba(99, 102, 241, 0.2) 0%, transparent 60%); pointer-events: none;
                    }
                    .overview-tag {
                        display: inline-flex; align-items: center; gap: 8px; background: rgba(99, 102, 241, 0.2);
                        color: #a5b4fc; padding: 8px 18px; border-radius: 30px; font-size: 0.85rem; font-weight: 800;
                        text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 20px; border: 1px solid rgba(99, 102, 241, 0.3);
                        backdrop-filter: blur(10px);
                    }
                    .overview-title {
                        font-size: 2.8rem; font-weight: 900; background: linear-gradient(to right, #ffffff, #a5b4fc);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 15px; letter-spacing: -0.02em;
                    }
                    .overview-desc {
                        color: #cbd5e1; font-size: 1.15rem; line-height: 1.7; max-width: 750px; margin-bottom: 35px;
                    }
                    .stats-container { display: flex; gap: 20px; flex-wrap: wrap; }
                    .stat-card {
                        flex: 1; min-width: 200px; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08);
                        border-radius: 16px; padding: 22px; display: flex; align-items: center; gap: 18px;
                        transition: all 0.3s ease; backdrop-filter: blur(10px);
                    }
                    .stat-card:hover {
                        background: rgba(255, 255, 255, 0.08); transform: translateY(-5px);
                        border-color: rgba(99, 102, 241, 0.5); box-shadow: 0 12px 24px rgba(0,0,0,0.2);
                    }
                    .stat-icon {
                        width: 52px; height: 52px; background: rgba(99, 102, 241, 0.15); color: #818cf8;
                        border-radius: 14px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(99, 102, 241, 0.2);
                    }
                    .stat-info strong { font-size: 1.3rem; display: block; color: white; margin-bottom: 5px; font-weight: 800; }
                    .stat-info span { font-size: 0.9rem; color: #94a3b8; font-weight: 500; }
                    
                    .rules-header {
                        font-size: 1.6rem; font-weight: 900; margin-bottom: 25px; display: flex; align-items: center; gap: 12px; color: var(--text-main);
                    }
                    .rules-header span {
                        background: linear-gradient(135deg, #6366f1, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                    }
                    .rule-card {
                        background: var(--bg-card); border: 1px solid var(--border); padding: 30px; border-radius: 20px;
                        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); position: relative; overflow: hidden;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
                    }
                    .rule-card::before {
                        content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 5px;
                        background: linear-gradient(90deg, #6366f1, #a855f7); opacity: 0; transition: opacity 0.3s ease;
                    }
                    .rule-card:hover {
                        transform: translateY(-8px); box-shadow: 0 20px 40px rgba(0,0,0,0.12); border-color: rgba(99, 102, 241, 0.3);
                    }
                    .rule-card:hover::before { opacity: 1; }
                    .rule-icon {
                        width: 54px; height: 54px; background: rgba(99, 102, 241, 0.1); color: #6366f1;
                        border-radius: 16px; display: flex; align-items: center; justify-content: center; margin-bottom: 20px;
                    }
                    .rule-card h4 { font-size: 1.25rem; font-weight: 800; color: var(--text-main); margin-bottom: 12px; letter-spacing: -0.01em; }
                    .rule-card p { font-size: 1.05rem; color: var(--text-muted); line-height: 1.7; margin: 0; }
                </style>

                <div class="overview-hero-p3">
                    <div class="overview-tag">
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                        Part 03: Short Conversations
                    </div>
                    <h2 class="overview-title">TỔNG QUAN NỘI DUNG PHẦN 03</h2>
                    <p class="overview-desc">Học cách nghe hiểu các cuộc đối thoại ngắn, nắm bắt từ khóa và phản xạ chọn đáp án nhanh chóng trong bài nghe.</p>
                    
                    <div class="stats-container">
                        <div class="stat-card">
                            <div class="stat-icon"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div>
                            <div class="stat-info">
                                <strong>39 Câu Hỏi</strong>
                                <span>Từ câu 32 đến câu 70</span>
                            </div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-icon"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></div>
                            <div class="stat-info">
                                <strong>13 Đoạn Thoại</strong>
                                <span>Cuộc trò chuyện ngắn</span>
                            </div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-icon"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></div>
                            <div class="stat-info">
                                <strong>2 - 3 Người</strong>
                                <span>Số lượng người nói</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="rules-header">
                    <svg viewBox="0 0 24 24" width="32" height="32" fill="none" stroke="#6366f1" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="9" y1="9" x2="15" y2="9"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="15" y2="17"/></svg> 
                    <span>CẤU TRÚC VÀ CÁC QUY TẮC TRỌNG TÂM</span>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px; margin-bottom: 40px;">
                    <div class="rule-card">
                        <div class="rule-icon"><svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></div>
                        <h4>13 Đoạn Hội Thoại</h4>
                        <p>Mỗi đoạn hội thoại gồm 03 câu hỏi đi kèm. Nội dung thường xoay quanh các tình huống trong công việc và đời sống hàng ngày như họp hành, mua sắm, dịch vụ...</p>
                    </div>
                    <div class="rule-card">
                        <div class="rule-icon"><svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a5 5 0 0 0-5 5v3.18a3 3 0 0 0-.58 1.7l1 5A3 3 0 0 0 10.38 18h3.24a3 3 0 0 0 3-2.12l1-5a3 3 0 0 0-.58-1.7V6a5 5 0 0 0-5-5z"/></svg></div>
                        <h4>Chỉ Được Nghe 1 Lần</h4>
                        <p>Thí sinh không được nghe lại lần thứ hai. Hãy tập trung cao độ ngay khi âm thanh bắt đầu phát và không phân tâm khi bỏ lỡ từ khóa.</p>
                    </div>
                    <div class="rule-card">
                        <div class="rule-icon"><svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div>
                        <h4>Tận Dụng Thời Gian Chờ</h4>
                        <p>Trong khi băng đọc câu hỏi, hãy tranh thủ đánh dấu đáp án và <strong>đọc trước bộ câu hỏi tiếp theo</strong> để dự đoán nội dung hội thoại sắp nghe.</p>
                    </div>
                </div>

            `;
            return;
        }
        
        const docContainer = document.createElement("div");
        docContainer.className = "theory-document";
        docContainer.style.background = "var(--bg-card)";
        docContainer.style.border = "1px solid var(--border)";
        docContainer.style.padding = "35px 40px";
        docContainer.style.color = "var(--text-main)";
        docContainer.style.lineHeight = "1.75";
        docContainer.style.textAlign = "left";
        
        let docHtml = "";
        
        section.theory.forEach((slide, sIdx) => {
            const lines = slide.text;
            if (!lines || lines.length === 0) return;
            
            const firstLine = lines[0].trim();
            const restLines = lines.slice(1);
            
            // Clean HTML tags to evaluate textual structure
            const cleanFirst = firstLine.replace(/<[^>]*>/g, "").trim();
            
            // Evaluates if the line acts as a divider or main section header
            const isMainHeader = cleanFirst.toUpperCase() === cleanFirst || /^\d+\.\s+/.test(cleanFirst) || cleanFirst.includes("CÂU HỎI") || cleanFirst.includes("LƯU Ý");
            
            if (isMainHeader) {
                // If it's a section header, draw a horizontal spacer above it (except for the first one)
                if (sIdx > 0) {
                    docHtml += `<hr style="border: none; border-top: 1px solid var(--border); margin: 40px 0 30px 0;">`;
                }
                
                docHtml += `
                    <h3 style="font-size: 1.35rem; font-weight: 700; color: var(--color-blue); margin: 0 0 24px 0; text-transform: uppercase; border-left: 4px solid var(--color-purple); padding-left: 14px; line-height: 1.4;">
                        ${firstLine}
                    </h3>
                `;
            } else {
                docHtml += `
                    <p style="font-size: 1.08rem; line-height: 1.7; color: var(--text-main); margin: 0 0 16px 0;">
                        ${firstLine}
                    </p>
                `;
            }
            
            restLines.forEach(line => {
                let cleanLine = line.trim();
                if (!cleanLine) return;
                
                // Match bullets, potentially preceded by leading HTML tags (e.g. <em>, <strong>)
                const htmlBulletRegex = /^((?:<[^>]+>\s*)*)(•|o|-|\*|◦)\s+/i;
                
                const bulletMatch = cleanLine.match(htmlBulletRegex);
                if (bulletMatch) {
                    const bulletChar = bulletMatch[2];
                    const cleanedHtml = cleanLine.replace(htmlBulletRegex, "$1").trim();
                    const isExample = bulletChar === "o" || bulletChar === "-";
                    const bulletClass = isExample ? "theory-bullet example-bullet" : "theory-bullet main-bullet";
                    
                    docHtml += `
                        <div class="${bulletClass}" style="margin-bottom: 12px;">
                            <span>${cleanedHtml}</span>
                        </div>
                    `;
                } else {
                    const rawText = cleanLine.replace(/<[^>]*>/g, "").trim();
                    const isSubHeader = ((cleanLine.startsWith("<strong>") && cleanLine.endsWith("</strong>")) || /^\d+(\.\d+)*\./.test(rawText)) && rawText.length < 120;
                    if (isSubHeader) {
                        docHtml += `
                            <h4 style="font-size: 1.15rem; font-weight: 700; color: var(--text-main); margin: 24px 0 12px 0; line-height: 1.4;">
                                ${cleanLine}
                            </h4>
                        `;
                    } else {
                        docHtml += `
                            <p style="font-size: 1.08rem; line-height: 1.7; color: var(--text-main); margin: 0 0 14px 0;">
                                ${cleanLine}
                            </p>
                        `;
                    }
                }
            });
        });
        
        docContainer.innerHTML = docHtml;
        theoryContentArea.appendChild(docContainer);
    }
     
    // B. VOCABULARY
    function renderVocabulary(section) {
        vocabularyContentArea.innerHTML = "";
        
        if (!section.vocabulary || section.vocabulary.length === 0) {
            vocabularyContentArea.innerHTML = "<p style='color: var(--text-muted); font-weight: 700;'>Không có từ vựng cho phần này.</p>";
            return;
        }
        
        section.vocabulary.forEach(slide => {
            const card = document.createElement("div");
            card.className = "vocabulary-card";
            
            const titleText = slide.text[0] || "Từ Vựng";
            const subtitleText = slide.text.length > 1 ? slide.text[1] : "";
            const bullets = slide.text.slice(2);
            
            let bulletsHtml = "";
            bullets.forEach(b => {
                let cleanB = b.trim();
                cleanB = cleanB.replace(/^(o|•|-|\*)\s+/, "");
                bulletsHtml += `
                    <li class="vocabulary-bullet">
                        <span>${cleanB}</span>
                    </li>
                `;
            });
            
            let subtitleHtml = "";
            if (subtitleText) {
                subtitleHtml = `<div class="vocabulary-card-subtitle">${subtitleText}</div>`;
            }
            
            card.innerHTML = `
                <div class="vocabulary-card-header">
                    <span class="vocabulary-card-title">${titleText}</span>
                    <span class="slide-num-tag">Slide ${slide.slide_index}</span>
                </div>
                ${subtitleHtml}
                <ul class="vocabulary-bullet-list">
                    ${bulletsHtml || `<li class="vocabulary-bullet"><span>${titleText}</span></li>`}
                </ul>
            `;
            
            vocabularyContentArea.appendChild(card);
        });
    }
    
    // C. EXAMPLES
    function renderExamples(section) {
        examplesContentArea.innerHTML = "";
        
        if (!section.examples || section.examples.length === 0) {
            examplesContentArea.innerHTML = "<p style='color: var(--text-muted); font-weight: 700;'>Không có câu hỏi ví dụ.</p>";
            return;
        }
        
        if (section.type === "topic" || section.type === "test") {
            // Render example sets for topics
            section.examples.forEach((set, setIdx) => {
                const setWrapper = document.createElement("div");
                setWrapper.className = "practice-set-card";
                setWrapper.style.padding = "24px";
                setWrapper.style.marginBottom = "24px";
                setWrapper.style.border = "1px solid var(--border)";
                setWrapper.style.background = "rgba(255, 255, 255, 0.01)";
                
                const setHeader = document.createElement("h3");
                setHeader.style.fontSize = "1.1rem";
                setHeader.style.marginBottom = "16px";
                setHeader.style.fontWeight = "800";
                setHeader.textContent = `VÍ DỤ MINH HỌA: ĐOẠN HỘI THOẠI ${set.set_index}`;
                setWrapper.appendChild(setHeader);
                
                const audioDiv = document.createElement("div");
                setWrapper.appendChild(audioDiv);
                createAudioPlayer(set.audio, audioDiv);
                
                const qListDiv = document.createElement("div");
                setWrapper.appendChild(qListDiv);
                
                const userSelections = {};
                const submitBtn = document.createElement("button");
                submitBtn.className = "btn btn-primary";
                submitBtn.style.margin = "20px 0";
                submitBtn.style.padding = "12px 24px";
                submitBtn.style.fontWeight = "700";
                submitBtn.style.borderRadius = "0px !important";
                submitBtn.textContent = "KIỂM TRA";
                submitBtn.disabled = true;

                set.questions.forEach(q => {
                    const qCard = document.createElement("div");
                    qCard.className = "question-block";
                    qCard.style.padding = "20px";
                    qCard.style.marginTop = "16px";
                    
                    const choicesHtml = renderChoicesHtml(q, false);
                    const questionTextHtml = renderQuestionTextHtml(q, `exset-q-${q.slide_index}`, `<strong>QUESTION ${q.id}:</strong> `);
                    
                    qCard.innerHTML = `
                        ${questionTextHtml}
                        <div class="choices-stack" style="margin-top: 12px;">
                            ${choicesHtml}
                        </div>
                    `;
                    
                    qListDiv.appendChild(qCard);
                    
                    const options = qCard.querySelectorAll(".choice-option");
                    options.forEach(opt => {
                        opt.addEventListener("click", () => {
                            if (opt.classList.contains("checked-done")) {
                                const t = opt.querySelector(".c-trans");
                                if (t) t.style.display = t.style.display === "block" ? "none" : "block";
                                return;
                            }
                            
                            // Toggle translation inline on click
                            const t = opt.querySelector(".c-trans");
                            if (t) t.style.display = t.style.display === "block" ? "none" : "block";
                            
                            const key = opt.getAttribute("data-key");
                            userSelections[q.slide_index] = key;
                            
                            options.forEach(o => o.classList.remove("selected"));
                            opt.classList.add("selected");
                            
                            let allSelected = true;
                            set.questions.forEach(qi => {
                                if (!userSelections[qi.slide_index]) {
                                    allSelected = false;
                                }
                            });
                            submitBtn.disabled = !allSelected;
                        });
                    });
                });
                
                setWrapper.appendChild(submitBtn);
                
                // Aggregate explanations
                let explanationHtml = "";
                set.questions.forEach(sq => {
                    if (sq.explanation) {
                        explanationHtml += `
                            <div class="explanation-box" style="margin-bottom: 16px; padding: 14px 18px; border: 1px solid var(--border); border-left: 4px solid var(--color-blue); background: rgba(59, 130, 246, 0.015);">
                                <h5 style="color: var(--color-blue); margin: 0 0 8px 0; font-size: 0.95rem; font-weight: 800; text-transform: uppercase;">
                                    Giải thích QUESTION ${sq.id}:
                                </h5>
                                <div style="font-size: 0.9rem; line-height: 1.5; color: var(--text-main);">
                                    ${sq.explanation}
                                </div>
                            </div>
                        `;
                    }
                });
                
                const transcriptHtml = renderTranscriptHtml(set.transcript, set.vietnamese_transcript);
                const scriptCard = document.createElement("div");
                scriptCard.innerHTML = renderScriptCardHtml(`exset-${set.set_index}`, transcriptHtml, explanationHtml);
                const innerScriptCard = scriptCard.firstElementChild;
                innerScriptCard.classList.add("hidden");
                
                setWrapper.appendChild(innerScriptCard);
                hookScriptCardToggler(`exset-${set.set_index}`);
                
                submitBtn.addEventListener("click", () => {
                    let setCorrectCount = 0;
                    set.questions.forEach(q => {
                        const key = userSelections[q.slide_index];
                        const qOptions = qListDiv.querySelectorAll(`.choice-option[data-q-slide="${q.slide_index}"]`);
                        qOptions.forEach(o => {
                            const oKey = o.getAttribute("data-key");
                            o.classList.remove("selected");
                            o.classList.add("checked-done");
                            if (oKey === q.answer) {
                                o.classList.add("correct");
                            } else if (oKey === key) {
                                o.classList.add("incorrect");
                            }
                        });
                        if (key === q.answer) {
                            spawnConfetti(25);
                            setCorrectCount++;
                        }
                    });
                    if (setCorrectCount >= 2) {
                        SoundEffects.playCorrect();
                    } else {
                        SoundEffects.playWrong();
                    }
                    innerScriptCard.classList.remove("hidden");
                    submitBtn.style.display = "none";
                });
                
                examplesContentArea.appendChild(setWrapper);
            });
        } else {
            // Render single examples for subsections
            section.examples.forEach((ex, exIdx) => {
                const wrapper = document.createElement("div");
                wrapper.className = "question-wrapper-group";
                wrapper.style.marginBottom = "24px";
                
                const audioDiv = document.createElement("div");
                wrapper.appendChild(audioDiv);
                createAudioPlayer(ex.audio, audioDiv);
                
                const qCard = document.createElement("div");
                qCard.className = "question-block";
                qCard.style.padding = "24px";
                
                const choicesHtml = renderChoicesHtml(ex, false);
                const questionTextHtml = renderQuestionTextHtml(ex, `ex-single-${ex.slide_index}`, `<strong>EXAMPLE ${exIdx + 1}:</strong> `);
                
                let explanationHtml = "";
                if (ex.explanation) {
                    explanationHtml = `
                        <div class="explanation-box" style="margin-bottom: 16px; padding: 14px 18px; border: 1px solid var(--border); border-left: 4px solid var(--color-blue); background: rgba(59, 130, 246, 0.015);">
                            <h5 style="color: var(--color-blue); margin: 0 0 8px 0; font-size: 0.95rem; font-weight: 800; text-transform: uppercase;">
                                GIẢI THÍCH ĐÁP ÁN:
                            </h5>
                            <div style="font-size: 0.9rem; line-height: 1.5; color: var(--text-main);">
                                ${ex.explanation}
                            </div>
                        </div>
                    `;
                }
                
                const transcriptHtml = renderTranscriptHtml(ex.transcript, ex.vietnamese_transcript);
                
                qCard.innerHTML = `
                    ${questionTextHtml}
                    <div class="choices-stack" style="margin-top: 16px;">
                        ${choicesHtml}
                    </div>
                    <div style="margin-top: 16px; text-align: right;">
                        <button class="btn btn-primary" id="btn-check-ex-${ex.slide_index}" style="padding: 10px 20px; font-weight: 700; border-radius: 0px !important;" disabled>KIỂM TRA</button>
                    </div>
                    ${renderScriptCardHtml(`ex-${ex.slide_index}`, transcriptHtml, explanationHtml)}
                `;
                
                wrapper.appendChild(qCard);
                examplesContentArea.appendChild(wrapper);
                hookScriptCardToggler(`ex-${ex.slide_index}`);
                
                const checkBtn = qCard.querySelector(`#btn-check-ex-${ex.slide_index}`);
                const options = qCard.querySelectorAll(".choice-option");
                let selectedKey = null;

                options.forEach(opt => {
                    opt.addEventListener("click", () => {
                        if (opt.classList.contains("checked-done")) {
                            const t = opt.querySelector(".c-trans");
                            if (t) t.style.display = t.style.display === "block" ? "none" : "block";
                            return;
                        }
                        
                        // Toggle option translation inline on click
                        const t = opt.querySelector(".c-trans");
                        if (t) t.style.display = t.style.display === "block" ? "none" : "block";
                        
                        selectedKey = opt.getAttribute("data-key");
                        options.forEach(o => o.classList.remove("selected"));
                        opt.classList.add("selected");
                        checkBtn.disabled = false;
                    });
                });

                checkBtn.addEventListener("click", () => {
                    options.forEach(o => {
                        const oKey = o.getAttribute("data-key");
                        o.classList.remove("selected");
                        o.classList.add("checked-done");
                        if (oKey === ex.answer) {
                            o.classList.add("correct");
                        } else if (oKey === selectedKey) {
                            o.classList.add("incorrect");
                        }
                    });
                    if (selectedKey === ex.answer) {
                        spawnConfetti(35);
                        SoundEffects.playCorrect();
                    } else {
                        SoundEffects.playWrong();
                    }
                    const scriptCardElement = qCard.querySelector(`#reveal-card-ex-${ex.slide_index}`);
                    if (scriptCardElement) scriptCardElement.classList.remove("hidden");
                    checkBtn.style.display = "none";
                });
            });
        }
    }
    
    // D. PRACTICE EXERCISES
    function renderPractice(section) {
        practiceContentArea.innerHTML = "";
        
        if (section.type === "subsection" || section.type === "overview" || section.type === "tips") {
            renderPracticeQuestions(section.practice, section);
        } else if (section.type === "topic" || section.type === "test") {
            renderPracticeSets(section.practice_sets, section);
        }
    }
    
    function renderPracticeQuestions(questions, section) {
        if (!questions || questions.length === 0) {
            practiceContentArea.innerHTML = "<p style='color: var(--text-muted); font-weight: 700;'>Bài tập đang được cập nhật.</p>";
            return;
        }

        // Initialize quiz state if needed
        if (!state.quiz.questions || state.quiz.sectionId !== section.id) {
            state.quiz = {
                sectionId: section.id,
                questions: questions,
                currentIdx: 0,
                score: 0,
                reviewMode: false,
                answers: {}
            };
        }

        if (state.quiz.reviewMode) {
            renderPracticeQuestionsReview(questions, section);
            return;
        }

        const currentIdx = state.quiz.currentIdx;
        
        if (currentIdx >= questions.length) {
            renderPracticeQuestionsSummary(questions, section);
            return;
        }

        const q = questions[currentIdx];
        practiceContentArea.innerHTML = "";

        // Progress Header
        const progressHeader = document.createElement("div");
        progressHeader.className = "quiz-progress-header";
        progressHeader.style.display = "flex";
        progressHeader.style.justifyContent = "space-between";
        progressHeader.style.alignItems = "center";
        progressHeader.style.marginBottom = "20px";
        progressHeader.style.padding = "14px 20px";
        progressHeader.style.background = "rgba(255, 255, 255, 0.015)";
        progressHeader.style.border = "1px solid var(--border)";
        
        const progressText = document.createElement("span");
        progressText.style.fontWeight = "700";
        progressText.style.fontSize = "0.9rem";
        progressText.style.color = "var(--text-main)";
        progressText.textContent = `CÂU HỎI ${currentIdx + 1} / ${questions.length}`;
        
        const scoreText = document.createElement("span");
        scoreText.className = "score-text-display";
        scoreText.style.fontWeight = "800";
        scoreText.style.fontSize = "0.95rem";
        scoreText.textContent = `ĐÚNG: ${state.quiz.score} / ${questions.length}`;
        
        progressHeader.appendChild(progressText);
        progressHeader.appendChild(scoreText);
        practiceContentArea.appendChild(progressHeader);

        // Active Question Card
        const wrapper = document.createElement("div");
        wrapper.className = "question-wrapper-group";
        wrapper.style.marginBottom = "24px";
        
        const audioDiv = document.createElement("div");
        wrapper.appendChild(audioDiv);
        createAudioPlayer(q.audio, audioDiv);
        
        const qCard = document.createElement("div");
        qCard.className = "question-block";
        qCard.style.padding = "24px";
        
        const choicesHtml = renderChoicesHtml(q, false);
        const questionTextHtml = renderQuestionTextHtml(q, `pr-${q.slide_index}`, `<strong>QUESTION:</strong> `);
        
        let explanationHtml = "";
        if (q.explanation) {
            explanationHtml = `
                <div class="explanation-box" style="margin-bottom: 16px; padding: 14px 18px; border: 1px solid var(--border); border-left: 4px solid var(--color-blue); background: rgba(59, 130, 246, 0.015);">
                    <h5 style="color: var(--color-blue); margin: 0 0 8px 0; font-size: 0.95rem; font-weight: 800; text-transform: uppercase;">
                        GIẢI THÍCH ĐÁP ÁN:
                    </h5>
                    <div style="font-size: 0.9rem; line-height: 1.5; color: var(--text-main);">
                        ${q.explanation}
                    </div>
                </div>
            `;
        }
        const transcriptHtml = renderTranscriptHtml(q.transcript, q.vietnamese_transcript);
        
        qCard.innerHTML = `
            ${questionTextHtml}
            <div class="choices-stack" style="margin-top: 16px;">
                ${choicesHtml}
            </div>
            ${renderScriptCardHtml(`pr-${q.slide_index}`, transcriptHtml, explanationHtml)}
            <div class="quiz-action-row" style="margin-top: 24px; display: flex; justify-content: space-between; align-items: center;">
                <button class="btn btn-primary" id="quiz-check-btn" style="padding: 12px 24px; font-weight: 700; border-radius: 0px !important;" disabled>
                    KIỂM TRA
                </button>
                <div style="flex:1;"></div>
                <button class="btn btn-primary" id="quiz-next-btn" style="display: none; padding: 12px 24px; font-weight: 700; border-radius: 0px !important; align-items: center; gap: 6px;">
                    CÂU TIẾP THEO <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle;"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </button>
            </div>
        `;
        
        wrapper.appendChild(qCard);
        practiceContentArea.appendChild(wrapper);
        hookScriptCardToggler(`pr-${q.slide_index}`);
        
        const checkBtn = qCard.querySelector("#quiz-check-btn");
        const nextBtn = qCard.querySelector("#quiz-next-btn");
        const options = qCard.querySelectorAll(".choice-option");
        let selectedKey = null;
        
        options.forEach(opt => {
            opt.addEventListener("click", () => {
                if (opt.classList.contains("checked-done")) {
                    const t = opt.querySelector(".c-trans");
                    if (t) t.style.display = t.style.display === "block" ? "none" : "block";
                    return;
                }
                
                // Toggle option translation inline on click
                const t = opt.querySelector(".c-trans");
                if (t) t.style.display = t.style.display === "block" ? "none" : "block";
                
                selectedKey = opt.getAttribute("data-key");
                options.forEach(o => o.classList.remove("selected"));
                opt.classList.add("selected");
                checkBtn.disabled = false;
            });
        });
        
        checkBtn.addEventListener("click", () => {
            state.quiz.answers[q.slide_index] = selectedKey;
            
            options.forEach(o => {
                const oKey = o.getAttribute("data-key");
                o.classList.remove("selected");
                o.classList.add("checked-done");
                if (oKey === q.answer) {
                    o.classList.add("correct");
                } else if (oKey === selectedKey) {
                    o.classList.add("incorrect");
                }
            });
            
            markQuestionAnswered(q.slide_index);
            
            const isCorrect = selectedKey === q.answer;
            if (isCorrect) {
                state.quiz.score++;
                scoreText.textContent = `ĐÚNG: ${state.quiz.score} / ${questions.length}`;
                spawnConfetti(35);
                SoundEffects.playCorrect();
            } else {
                SoundEffects.playWrong();
            }
            
            // Submit to Google Forms background
            const studentName = localStorage.getItem("studentName") || "Ẩn danh";
            submitToGoogleForm(studentName, `${section.title} - Câu ${currentIdx + 1}`, "Luyện tập (Câu)", isCorrect ? 1 : 0, 1);
            
            const scriptCardElement = qCard.querySelector(`#reveal-card-pr-${q.slide_index}`);
            if (scriptCardElement) scriptCardElement.classList.remove("hidden");
            
            checkBtn.style.display = "none";
            nextBtn.style.display = "flex";
        });
        
        nextBtn.addEventListener("click", () => {
            state.quiz.currentIdx++;
            renderPracticeQuestions(questions, section);
        });
    }

    function renderPracticeQuestionsSummary(questions, section) {
        practiceContentArea.innerHTML = "";
        
        const score = state.quiz.score;
        const total = questions.length;
        
        let msg = "";
        if (score === total) {
            msg = "QUÁ XUẤT SẮC! Bạn đã trả lời đúng toàn bộ câu hỏi. Hãy tiếp tục phát huy phong độ này nhé!";
            let count = 0;
            const interval = setInterval(() => {
                spawnConfetti(45, true); // Gold only
                count++;
                if (count > 5) clearInterval(interval);
            }, 400);
        } else if (score >= total * 0.7) {
            msg = "RẤT TỐT! Kỹ năng nghe của bạn khá vững vàng. Hãy xem lại các câu sai để rút kinh nghiệm nhé.";
            spawnConfetti(50);
        } else {
            msg = "CỐ GẮNG LÊN! Bạn cần luyện tập thêm. Hãy dành thời gian xem lại transcript và từ vựng của dạng bài này.";
        }
        
        const summaryCard = document.createElement("div");
        summaryCard.className = "quiz-summary-card";
        summaryCard.style.textAlign = "center";
        summaryCard.style.padding = "48px 40px";
        summaryCard.style.border = "1px solid var(--border)";
        summaryCard.style.background = "rgba(255, 255, 255, 0.015)";
        
        summaryCard.innerHTML = `
            <div style="font-size: 3.5rem; color: var(--color-gold); margin-bottom: 20px;">🏆</div>
            <h3 style="font-size: 1.6rem; margin-bottom: 12px; font-weight: 800; text-transform: uppercase;">KẾT QUẢ BÀI TẬP</h3>
            <div style="font-size: 2.8rem; font-weight: 800; color: var(--color-blue); margin-bottom: 16px;">
                ${score} / ${total}
            </div>
            <p style="color: var(--text-muted); font-size: 1.05rem; margin-bottom: 36px; line-height: 1.7; max-width: 500px; margin-left: auto; margin-right: auto;">${msg}</p>
            <div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap;">
                <button class="btn btn-primary" id="btn-quiz-retry" style="padding: 12px 24px; font-weight: 700; border-radius: 0px !important;">LÀM LẠI BÀI TẬP</button>
                <button class="btn btn-secondary" id="btn-quiz-review" style="padding: 12px 24px; font-weight: 700; border-radius: 0px !important;">XEM LẠI ĐÁP ÁN</button>
            </div>
        `;
        
        practiceContentArea.appendChild(summaryCard);
        
        document.getElementById("btn-quiz-retry").addEventListener("click", () => {
            state.quiz = {
                sectionId: section.id,
                questions: questions,
                currentIdx: 0,
                score: 0,
                reviewMode: false,
                answers: {}
            };
            // Clear progress
            questions.forEach(q => {
                delete state.answeredQuestions[q.slide_index];
            });
            updateRouteProgress();
            try {
                localStorage.setItem("toeic_answered_questions", JSON.stringify(state.answeredQuestions));
            } catch (e) {}
            
            renderPracticeQuestions(questions, section);
        });
        
        document.getElementById("btn-quiz-review").addEventListener("click", () => {
            state.quiz.reviewMode = true;
            renderPracticeQuestions(questions, section);
        });
    }

    function renderPracticeQuestionsReview(questions, section) {
        practiceContentArea.innerHTML = "";
        
        // Review Header
        const reviewHeader = document.createElement("div");
        reviewHeader.className = "quiz-progress-header";
        reviewHeader.style.display = "flex";
        reviewHeader.style.justifyContent = "space-between";
        reviewHeader.style.alignItems = "center";
        reviewHeader.style.marginBottom = "24px";
        reviewHeader.style.padding = "14px 20px";
        reviewHeader.style.background = "rgba(255, 255, 255, 0.015)";
        reviewHeader.style.border = "1px solid var(--border)";
        
        const reviewTitle = document.createElement("span");
        reviewTitle.style.fontWeight = "700";
        reviewTitle.style.fontSize = "0.9rem";
        reviewTitle.textContent = "XEM LẠI ĐÁP ÁN & TRANSCRIPT";
        
        const backBtn = document.createElement("button");
        backBtn.className = "mini-btn";
        backBtn.style.padding = "6px 12px";
        backBtn.textContent = "QUAY LẠI TỔNG KẾT";
        backBtn.style.borderRadius = "0px !important";
        backBtn.addEventListener("click", () => {
            state.quiz.currentIdx = questions.length; // triggers summary view
            renderPracticeQuestions(questions, section);
        });
        
        reviewHeader.appendChild(reviewTitle);
        reviewHeader.appendChild(backBtn);
        practiceContentArea.appendChild(reviewHeader);

        // List all questions
        questions.forEach((q, idx) => {
            const wrapper = document.createElement("div");
            wrapper.className = "question-wrapper-group";
            wrapper.style.marginBottom = "28px";
            
            const audioDiv = document.createElement("div");
            wrapper.appendChild(audioDiv);
            createAudioPlayer(q.audio, audioDiv);
            
            const qCard = document.createElement("div");
            qCard.className = "question-block";
            qCard.style.padding = "24px";
            
            const userAnswer = state.quiz.answers[q.slide_index];
            const choicesHtml = renderChoicesHtml(q, true, userAnswer);
            
            let badgeText = userAnswer === q.answer ? 
                `<span style="color: var(--success); margin-left: 10px; font-size: 0.9rem; font-weight: 700;">✔️ ĐÚNG</span>` : 
                `<span style="color: var(--danger); margin-left: 10px; font-size: 0.85rem; font-weight: 700;">❌ SAI (Chọn ${userAnswer || "Trống"})</span>`;
            
            const questionTextHtml = renderQuestionTextHtml(q, `rev-q-${q.slide_index}`, `<strong>QUESTION ${idx + 1}:</strong> `);
            
            let explanationHtml = "";
            if (q.explanation) {
                explanationHtml = `
                    <div class="explanation-box" style="margin-bottom: 16px; padding: 14px 18px; border: 1px solid var(--border); border-left: 4px solid var(--color-blue); background: rgba(59, 130, 246, 0.015);">
                        <h5 style="color: var(--color-blue); margin: 0 0 8px 0; font-size: 0.95rem; font-weight: 800; text-transform: uppercase;">
                            GIẢI THÍCH ĐÁP ÁN:
                        </h5>
                        <div style="font-size: 0.9rem; line-height: 1.5; color: var(--text-main);">
                            ${q.explanation}
                        </div>
                    </div>
                `;
            }
            const transcriptHtml = renderTranscriptHtml(q.transcript, q.vietnamese_transcript);
            
            qCard.innerHTML = `
                <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom: 10px; width:100%;">
                    <div style="flex:1;">${questionTextHtml}</div>
                    <div>${badgeText}</div>
                </div>
                <div class="choices-stack" style="margin-top: 16px;">
                    ${choicesHtml}
                </div>
                ${renderScriptCardHtml(`rev-${q.slide_index}`, transcriptHtml, explanationHtml)}
            `;
            
            wrapper.appendChild(qCard);
            practiceContentArea.appendChild(wrapper);
            
            const revCard = qCard.querySelector(`.reveal-script-card`);
            if (revCard) revCard.classList.remove("hidden");
            hookScriptCardToggler(`rev-${q.slide_index}`);
        });
    }

    // E. PRACTICE SETS (FOR TOPICS)

    function renderPracticeSets(sets, section) {
        if (!practiceContentArea) return;
        
        if (!window.checkP1PracticeAnswer) {
            window.checkP1PracticeAnswer = function(exId, selectedKey, correctKey) {
                const card = document.getElementById(exId);
                if (!card) return;
                
                const btns = card.querySelectorAll('.p1-interactive-btn');
                btns.forEach(btn => {
                    btn.style.pointerEvents = 'none';
                    if (btn.id === `btn-${exId}-${correctKey}`) {
                        btn.classList.add('correct');
                    } else if (btn.id === `btn-${exId}-${selectedKey}` && selectedKey !== correctKey) {
                        btn.classList.add('incorrect');
                    }
                });
                
                const transcript = card.querySelector('.p1-ex-transcript');
                if (transcript) {
                    transcript.style.display = 'block';
                    transcript.style.animation = 'fadeIn 0.5s ease forwards';
                }
                
                const correctChoice = document.getElementById(`transcript-choice-${exId}-${correctKey}`);
                if (correctChoice) correctChoice.classList.add('highlight-correct');
            };
        }
        
        let html = `
            <style>
                @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
                .p1-ex-card {
                    background: var(--bg-card); border: 1px solid rgba(255,255,255,0.08); padding: 30px; border-radius: 24px;
                    margin-bottom: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); transition: all 0.4s ease;
                    backdrop-filter: blur(10px); display: flex; flex-direction: column; align-items: center;
                }
                .p1-ex-card:hover { border-color: rgba(99, 102, 241, 0.4); box-shadow: 0 15px 35px rgba(0,0,0,0.15); }
                
                .p1-image-container { width: 100%; max-width: 500px; margin-bottom: 25px; border-radius: 12px; overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
                .p1-image-container img { width: 100%; height: auto; display: block; object-fit: cover; }
                
                .p1-audio-player { text-align: center; margin-bottom: 25px; width: 100%; }
                
                .p1-interactive-buttons { display: flex; justify-content: center; gap: 20px; margin-bottom: 10px; flex-wrap: wrap; }
                .p1-interactive-btn {
                    background: rgba(255,255,255,0.03); border: 2px solid rgba(255,255,255,0.15); color: var(--text-main);
                    width: 65px; height: 65px; border-radius: 50%; font-size: 1.25rem; font-weight: 800;
                    cursor: pointer; transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
                    display: flex; align-items: center; justify-content: center; outline: none;
                }
                .p1-interactive-btn:hover { background: rgba(99, 102, 241, 0.1); border-color: #6366f1; transform: scale(1.1); color: #818cf8; }
                .p1-interactive-btn.correct { background: #16a34a; border-color: #15803d; color: white; transform: scale(1.1); box-shadow: 0 0 15px rgba(22, 163, 74, 0.5); }
                .p1-interactive-btn.incorrect { background: #dc2626; border-color: #b91c1c; color: white; transform: scale(0.95); opacity: 0.8; }
                
                .p1-ex-transcript {
                    margin-top: 25px; padding-top: 25px; border-top: 1px dashed rgba(255,255,255,0.15); width: 100%;
                }
                .p1-ex-transcript-choices { display: flex; flex-direction: column; gap: 10px; }
                .p1-ex-transcript-choice {
                    display: flex; gap: 15px; font-size: 1.1rem; color: var(--text-muted); padding: 12px 18px;
                    border-radius: 12px; background: var(--border); transition: all 0.3s ease; border: 1px solid transparent;
                }
                .p1-ex-transcript-choice .lbl { font-weight: 900; color: #94a3b8; min-width: 25px; }
                .p1-ex-transcript-choice.highlight-correct {
                    background: rgba(34, 197, 94, 0.1); color: #4ade80; border-color: rgba(34, 197, 94, 0.3);
                }
                .p1-ex-transcript-choice.highlight-correct .lbl { color: #4ade80; }
            </style>
            
            <div class="p2-hero" style="background: radial-gradient(circle at 0% 0%, rgba(99, 102, 241, 0.15) 0%, transparent 50%), linear-gradient(145deg, #0f172a 0%, #020617 100%); margin-bottom: 30px; border-radius: 16px; padding: 24px;">
                <h2 class="p2-hero-title" style="text-align: center; color: #f8fafc; font-weight: 800; font-size: 1.5rem; margin-bottom: 8px;">LUYỆN TẬP TƯƠNG TÁC</h2>
                <p class="p2-hero-subtitle" style="text-align: center; color: #94a3b8;">Bấm nút PLAY để nghe Audio. Sau đó chọn đáp án A, B, C hoặc D. Hệ thống sẽ chấm điểm và hiển thị nội dung chi tiết.</p>
            </div>
        `;
        
        if (!sets || sets.length === 0) {
            html += "<p style='color: var(--text-muted); padding: 20px;'>Bài tập đang được cập nhật.</p>";
            practiceContentArea.innerHTML = html;
            return;
        }
        
        sets.forEach((setObj, index) => {
            const exId = `p1-ex-${section.id}-${index}`;
            // Assuming setObj has image, audio, and questions[0]
            const q = setObj.questions && setObj.questions[0];
            if (!q) return;
            
            const correctAns = q.answer || 'A';
            
            const imageHtml = setObj.image ? `
                <div class="p1-image-container">
                    <img src="${setObj.image}" alt="Question Image" onerror="this.src='media/${setObj.image}'">
                </div>
            ` : '';
            
            const audioHtml = setObj.audio ? `
                <div class="p1-audio-player">
                    <audio id="audio-${exId}" src="media/${setObj.audio}" controls style="width: 100%; max-width: 400px; border-radius: 50px; outline: none;"></audio>
                </div>
            ` : `<div class="p1-audio-player"><p style="color:#ef4444;">[Thiếu Audio]</p></div>`;
            
            let interactiveButtons = '<div class="p1-interactive-buttons">';
            let transcriptChoicesHtml = '<div class="p1-ex-transcript-choices">';
            
            if (q.choices) {
                Object.keys(q.choices).forEach(key => {
                    interactiveButtons += `
                        <button class="p1-interactive-btn" id="btn-${exId}-${key}" 
                                onclick="window.checkP1PracticeAnswer('${exId}', '${key}', '${correctAns}')">
                            ${key}
                        </button>
                    `;
                    transcriptChoicesHtml += `
                        <div class="p1-ex-transcript-choice" id="transcript-choice-${exId}-${key}">
                            <span class="lbl">(${key})</span> <span class="txt">${q.choices[key]}</span>
                        </div>
                    `;
                });
            }
            interactiveButtons += '</div>';
            transcriptChoicesHtml += '</div>';

            let vocabHtml = '';
            if (q.vocabulary && q.vocabulary.length > 0) {
                let vocabItems = q.vocabulary.map(v => `
                    <div style="margin-bottom: 8px; font-size: 1.05rem;">
                        <span style="font-weight: 700; color: #0284c7;">${v.pos === 'v' && v.base && v.gerund && v.base !== v.gerund ? `${v.base} ➔ ${v.gerund}` : v.en}</span> 
                        <span style="color: #64748b; font-size: 0.9em; font-family: monospace;">${v.ipa}</span>
                        <span style="color: #a855f7; font-size: 0.9em; font-style: italic;">(${v.pos})</span>: 
                        <span style="color: var(--text-main);">${v.vi}</span>
                        <span onclick="playTTS(this.dataset.text, event)" data-text="${(v.pos === 'v' && v.base && v.gerund && v.base !== v.gerund ? v.base + ', ' + v.gerund : (v.base || v.en)).replace(/"/g, '&quot;')}" style="cursor: pointer; margin-left: 6px; opacity: 0.6; font-size: 1.1em;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.6'" title="Đọc từ này">🔊</span>
                    </div>
                `).join('');
                vocabHtml = `
                    <div class="p1-vocab-box" style="margin-top: 20px; padding: 18px 20px; border-radius: 12px; background: var(--bg-sidebar); border: 1px solid var(--border); box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);">
                        <h4 style="font-weight: 800; font-size: 1.1rem; color: #10b981; margin-bottom: 15px; display: flex; align-items: center; gap: 8px; text-transform: uppercase;">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>
                            Từ vựng hữu ích
                        </h4>
                        ${vocabItems}
                    </div>
                `;
            }
            
            html += `
                <div class="p1-ex-card" id="${exId}">
                    <h3 style="align-self: flex-start; margin-bottom: 20px; font-weight: 800; color: var(--text-main);">QUESTION ${q.id}</h3>
                    ${imageHtml}
                    ${audioHtml}
                    ${interactiveButtons}
                    
                    <div class="p1-ex-transcript" id="transcript-${exId}" style="display: none;">
                        ${transcriptChoicesHtml}
                        ${vocabHtml}
                    </div>
                </div>
            `;
        });
        
        practiceContentArea.innerHTML = html;
    }




// ================= PART 02 FUNCTIONS =================
    function initializePart02Sidebar() {
        if (!part2ConceptsNavList) return;
        
        part2ConceptsNavList.innerHTML = "";
        const isUnlocked = window.isUnlocked;
        
        if (typeof categoryTreeP2 !== "undefined") {
            categoryTreeP2.forEach(node => {
                if (node.type === "item") {
                    const submenuItem = document.createElement("div");
                    submenuItem.className = "submenu-item";
                    submenuItem.setAttribute("data-id", node.id);
                    
                    let text = node.title.toUpperCase();
                    if (LOCKED_SECTIONS.includes(node.id) && !isUnlocked) {
                        text += " 🔒";
                    }
                    submenuItem.textContent = text;
                    
                    submenuItem.addEventListener("click", (e) => {
                        e.stopPropagation();
                        loadSectionP2(node.id);
                    });
                    part2ConceptsNavList.appendChild(submenuItem);
                } else if (node.type === "group") {
                    // Render group header
                    const groupHeader = document.createElement("div");
                    groupHeader.className = "sidebar-group-header";
                    groupHeader.textContent = node.title.toUpperCase();
                    part2ConceptsNavList.appendChild(groupHeader);
                    
                    // Render items inside group
                    node.items.forEach(item => {
                        const submenuItem = document.createElement("div");
                        submenuItem.className = "submenu-item group-item";
                        submenuItem.setAttribute("data-id", item.id);
                        
                        let text = item.title.toUpperCase();
                        if (LOCKED_SECTIONS.includes(item.id) && !isUnlocked) {
                            text += " 🔒";
                        }
                        submenuItem.textContent = text;
                        
                        submenuItem.addEventListener("click", (e) => {
                            e.stopPropagation();
                            loadSectionP2(item.id);
                        });
                        part2ConceptsNavList.appendChild(submenuItem);
                    });
                }
            });
        }
    }

    function loadSectionP2(sectionId) {
        if (LOCKED_SECTIONS.includes(sectionId) && !window.isUnlocked) {
            if (window.showPaywallModal) window.showPaywallModal();
            return;
        }
        
        state.part02ActiveSection = sectionId;
        
        if (part2ConceptsNavList) {
            const items = part2ConceptsNavList.querySelectorAll('.submenu-item');
            items.forEach(el => {
                if (el.getAttribute('data-id') === sectionId) {
                    el.classList.add('active');
                    if (breadCurrentP2) breadCurrentP2.textContent = el.textContent.replace(' 🔒', '');
                    if (panelTitleP2) panelTitleP2.textContent = el.textContent.replace(' 🔒', '');
                } else {
                    el.classList.remove('active');
                }
            });
        }
        
        if (!window.part02Data) {
            console.error("part02Data is not loaded");
            return;
        }
        
        const section = window.part02Data.find(s => s.id === sectionId);
        if (!section) return;
        
        // Hide unused buttons
        if (secBtnTheoryP2) secBtnTheoryP2.classList.remove("hidden");
        if (secBtnExamplesP2) secBtnExamplesP2.classList.remove("hidden");
        if (secBtnVocabularyP2) secBtnVocabularyP2.classList.add("hidden");
        if (secBtnPracticeP2) secBtnPracticeP2.classList.add("hidden");
        
        renderTheoryP2(section);
        renderExamplesP2(section);
        
        if (secBtnTheoryP2) secBtnTheoryP2.click();
    }

    function renderTheoryP2(section) {
        if (!theoryContentAreaP2) return;
        
        let html = `
            <style>
                .p2-hero {
                    background: radial-gradient(circle at 100% 100%, rgba(99, 102, 241, 0.15) 0%, transparent 50%), linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
                    color: white; padding: 45px 50px; border-radius: 24px; position: relative; overflow: hidden;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.3); margin-bottom: 40px; border: 1px solid rgba(255, 255, 255, 0.05);
                }
                .p2-hero::after {
                    content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                    background: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0IiBoZWlnaHQ9IjQiPgo8cmVjdCB3aWR0aD0iNCIgaGVpZ2h0PSI0IiBmaWxsPSIjZmZmIiBmaWxsLW9wYWNpdHk9IjAuMDUiLz4KPC9zdmc+') repeat;
                    opacity: 0.3; pointer-events: none;
                }
                .p2-hero-title { font-size: 2.6rem; font-weight: 900; margin-bottom: 15px; color: #f8fafc; letter-spacing: -0.02em; }
                .p2-hero-subtitle { font-size: 1.15rem; color: #94a3b8; line-height: 1.7; max-width: 650px; font-weight: 400; }
                
                .p2-theory-card {
                    background: var(--bg-card); border: 1px solid rgba(255,255,255,0.08); padding: 35px; border-radius: 24px;
                    transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); position: relative; overflow: hidden;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1); margin-bottom: 30px;
                    backdrop-filter: blur(10px);
                }
                .p2-theory-card::before {
                    content: ''; position: absolute; top: 0; left: 0; width: 6px; height: 100%;
                    background: linear-gradient(180deg, #6366f1, #a855f7); opacity: 0; transition: opacity 0.3s ease;
                }
                .p2-theory-card:hover {
                    transform: translateY(-8px); box-shadow: 0 25px 50px rgba(0,0,0,0.2); border-color: rgba(99, 102, 241, 0.4);
                }
                .p2-theory-card:hover::before { opacity: 1; }
                .p2-theory-title {
                    font-size: 1.4rem; font-weight: 800; color: var(--text-main); margin-bottom: 25px; display: flex; align-items: center; gap: 16px;
                }
                .p2-theory-title .icon {
                    width: 48px; height: 48px; background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(168, 85, 247, 0.2)); color: #818cf8;
                    border-radius: 14px; display: flex; align-items: center; justify-content: center;
                    border: 1px solid rgba(99, 102, 241, 0.3);
                }
                .p2-theory-content {
                    display: flex; flex-direction: column; gap: 15px; padding: 0; margin: 0;
                }
                .p2-text-line {
                    font-size: 1.1rem; color: var(--text-muted); line-height: 1.8; margin: 0; padding-left: 5px;
                }
                .p2-text-highlight {
                    color: var(--text-main); font-weight: 600; background: rgba(99, 102, 241, 0.08);
                    padding: 18px 24px; border-radius: 16px; border: 1px solid rgba(99, 102, 241, 0.2);
                    box-shadow: inset 0 2px 4px rgba(0,0,0,0.05); margin-top: 5px; margin-bottom: 5px;
                    font-size: 1.1rem; line-height: 1.8;
                }
                .p2-theory-content img {
                    max-width: 100%; border-radius: 12px; margin: 10px 0;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                }
            </style>
            
            <div class="p2-hero">
                <h2 class="p2-hero-title">${section.title.replace(/^[0-9IV]+\.\s*/, '')}</h2>
                <p class="p2-hero-subtitle">Nắm vững kiến thức, các dạng câu hỏi và mẹo nhận biết đáp án để chinh phục Phần 2 TOEIC Listening dễ dàng hơn.</p>
            </div>
        `;
        
        if (!section.theory || section.theory.length === 0) {
            html += "<p style='color: var(--text-muted); padding: 20px;'>Nội dung đang được cập nhật...</p>";
            theoryContentAreaP2.innerHTML = html;
            return;
        }
        
        section.theory.forEach(t => {
            if (!t.text || t.text.length === 0) return;
            
            let titleHtml = '';
            let contentLines = t.text;
            
            // Only use the first line as a title if it's text, not an image
            if (!t.text[0].trim().toLowerCase().startsWith('<img')) {
                titleHtml = `
                    <div class="p2-theory-title">
                        <div class="icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg></div>
                        ${t.text[0]}
                    </div>
                `;
                contentLines = t.text.slice(1);
            }
            
            let listHtml = '';
            contentLines.forEach(line => {
                if (line.startsWith('👉') || line.toLowerCase().includes('ví dụ') || line.toLowerCase().includes('ví dụ:')) {
                    listHtml += `<div class="p2-text-highlight">${line.replace('👉', '').trim()}</div>`;
                } else if (line.trim().toLowerCase().startsWith('<img')) {
                    listHtml += line; // render image block directly
                } else {
                    listHtml += `<p class="p2-text-line">${line}</p>`;
                }
            });
            
            html += `
                <div class="p2-theory-card">
                    ${titleHtml}
                    <div class="p2-theory-content">
                        ${listHtml}
                    </div>
                </div>
            `;
        });
        
        if (section.vocabulary && section.vocabulary.length > 0) {
            let vocabItems = section.vocabulary.map(v => {
                let txt = v.en;
                if (v.pos === 'v' && v.base && v.gerund && v.base !== v.gerund) txt = `${v.base} ➔ ${v.gerund}`;
                let ttsTxt = v.en;
                if (v.pos === 'v' && v.base && v.gerund && v.base !== v.gerund) ttsTxt = `${v.base}, ${v.gerund}`;
                
                return `
                <div style="margin-bottom: 12px; font-size: 1.15rem; line-height: 1.6; padding-bottom: 8px; border-bottom: 1px dashed rgba(255,255,255,0.05);">
                    <span style="font-weight: 800; color: #0ea5e9;">${txt}</span> 
                    <span style="color: #94a3b8; font-size: 0.95em; font-family: monospace;">${v.ipa}</span>
                    <span style="color: #a855f7; font-size: 0.95em; font-style: italic;">(${v.pos || 'n'})</span>: 
                    <span style="color: var(--text-main); font-weight: 500;">${v.vi}</span>
                    <span onclick="playTTS(this.dataset.text, event)" data-text="${ttsTxt.replace(/"/g, '&quot;')}" style="cursor: pointer; margin-left: 10px; font-size: 1.2rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2)); transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.2)'" onmouseout="this.style.transform='scale(1)'" title="Đọc từ này">🔊</span>
                </div>
                `;
            }).join('');
            
            html += `
                <div class="p2-theory-card" style="border-color: rgba(16, 185, 129, 0.3);">
                    <div class="p2-theory-title" style="color: #10b981; font-size: 1.5rem;">
                        <div class="icon" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(52, 211, 153, 0.2)); color: #10b981; border-color: rgba(16, 185, 129, 0.3);">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>
                        </div>
                        TỪ VỰNG TRỌNG TÂM
                    </div>
                    <div class="p2-theory-content" style="background: rgba(0,0,0,0.2); padding: 25px; border-radius: 16px;">
                        ${vocabItems}
                    </div>
                </div>
            `;
        }
        
        theoryContentAreaP2.innerHTML = html;
    }

    function renderExamplesP2(section) {
        if (!examplesContentAreaP2) return;
        
        if (!window.checkP2ExampleAnswer) {
            window.checkP2ExampleAnswer = function(exId, selectedKey, correctKey) {
                const card = document.getElementById(exId);
                if (!card) return;
                
                const btns = card.querySelectorAll('.p2-interactive-btn');
                btns.forEach(btn => {
                    btn.style.pointerEvents = 'none';
                    if (btn.id === `btn-${exId}-${correctKey}`) {
                        btn.classList.add('correct');
                    } else if (btn.id === `btn-${exId}-${selectedKey}` && selectedKey !== correctKey) {
                        btn.classList.add('incorrect');
                    }
                });
                
                const transcript = card.querySelector('.p2-ex-transcript');
                if (transcript) {
                    transcript.style.display = 'block';
                    transcript.style.animation = 'fadeIn 0.5s ease forwards';
                }
                
                const correctChoice = document.getElementById(`transcript-choice-${exId}-${correctKey}`);
                if (correctChoice) correctChoice.classList.add('highlight-correct');
            };
        }
        
        let html = `
            <style>
                @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
                .p2-ex-card {
                    background: var(--bg-card); border: 1px solid rgba(255,255,255,0.08); padding: 40px; border-radius: 24px;
                    margin-bottom: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); transition: all 0.4s ease;
                    backdrop-filter: blur(10px);
                }
                .p2-ex-card:hover { border-color: rgba(99, 102, 241, 0.4); box-shadow: 0 15px 35px rgba(0,0,0,0.15); }
                
                .p2-audio-player { text-align: center; margin-bottom: 30px; }
                .p2-play-btn {
                    background: linear-gradient(135deg, #6366f1, #a855f7); color: white; border: none;
                    padding: 14px 30px; border-radius: 50px; font-size: 1.15rem; font-weight: 700; letter-spacing: 0.5px;
                    cursor: pointer; display: inline-flex; align-items: center; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
                    transition: all 0.3s ease;
                }
                .p2-play-btn:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(99, 102, 241, 0.6); }
                
                .p2-interactive-buttons { display: flex; justify-content: center; gap: 25px; margin-bottom: 20px; }
                .p2-interactive-btn {
                    background: rgba(255,255,255,0.03); border: 2px solid rgba(255,255,255,0.15); color: var(--text-main);
                    width: 75px; height: 75px; border-radius: 50%; font-size: 1.4rem; font-weight: 800;
                    cursor: pointer; transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
                    display: flex; align-items: center; justify-content: center; outline: none;
                }
                .p2-interactive-btn:hover { background: rgba(99, 102, 241, 0.1); border-color: #6366f1; transform: scale(1.1); color: #818cf8; }
                .p2-interactive-btn.correct { background: #16a34a; border-color: #15803d; color: white; transform: scale(1.1); box-shadow: 0 0 20px rgba(22, 163, 74, 0.5); }
                .p2-interactive-btn.incorrect { background: #dc2626; border-color: #b91c1c; color: white; transform: scale(0.95); opacity: 0.8; }
                
                .p2-ex-transcript {
                    margin-top: 35px; padding-top: 25px; border-top: 1px dashed rgba(255,255,255,0.15);
                }
                .p2-ex-question-text {
                    font-size: 1.25rem; font-weight: 800; color: var(--text-main); margin-bottom: 20px; line-height: 1.6;
                }
                .p2-ex-transcript-choices { display: flex; flex-direction: column; gap: 12px; }
                .p2-ex-transcript-choice {
                    display: flex; gap: 15px; font-size: 1.15rem; color: var(--text-muted); padding: 14px 20px;
                    border-radius: 12px; background: rgba(0,0,0,0.15); transition: all 0.3s ease; border: 1px solid transparent;
                }
                .p2-ex-transcript-choice .lbl { font-weight: 900; color: #94a3b8; }
                .p2-ex-transcript-choice.highlight-correct {
                    background: rgba(34, 197, 94, 0.1); color: #4ade80; border-color: rgba(34, 197, 94, 0.3);
                }
                .p2-ex-transcript-choice.highlight-correct .lbl { color: #4ade80; }
            </style>
            
            <div class="p2-hero" style="background: radial-gradient(circle at 0% 0%, rgba(168, 85, 247, 0.15) 0%, transparent 50%), linear-gradient(145deg, #0f172a 0%, #020617 100%); border-radius: 16px; padding: 24px;">
                <h2 class="p2-hero-title" style="color: #f8fafc; font-weight: 800; font-size: 1.5rem; margin-bottom: 8px;">VÍ DỤ THỰC HÀNH</h2>
                <p class="p2-hero-subtitle" style="color: #94a3b8;">Mô phỏng 100% format bài thi thật: Bấm nghe audio, chọn đáp án A, B hoặc C. Sau khi chọn xong, hệ thống sẽ đối chiếu và hiện bản dịch chi tiết.</p>
            </div>
        `;
        
        if (!section.examples || section.examples.length === 0) {
            html += "<p style='color: var(--text-muted); padding: 20px;'>Không có ví dụ nào cho phần này.</p>";
            examplesContentAreaP2.innerHTML = html;
            return;
        }
        
        section.examples.forEach((ex, index) => {
            const exId = `p2-ex-${section.id}-${index}`;
            const correctAns = ex.answer || 'B';
            
            const audioHtml = ex.audio ? `
                <div class="p2-audio-player">
                    <audio id="audio-${exId}" src="${ex.audio}"></audio>
                    <button class="p2-play-btn" onclick="document.getElementById('audio-${exId}').play()">
                        <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" style="margin-right: 8px;"><path d="M8 5v14l11-7z"/></svg> 
                        Nghe Audio Ví Dụ ${index + 1}
                    </button>
                </div>
            ` : `<div class="p2-audio-player"><p style="color:#ef4444;">[Thiếu Audio]</p></div>`;
            
            let interactiveButtons = '<div class="p2-interactive-buttons">';
            let transcriptChoicesHtml = '<div class="p2-ex-transcript-choices">';
            
            if (ex.choices) {
                Object.keys(ex.choices).forEach(key => {
                    interactiveButtons += `
                        <button class="p2-interactive-btn" id="btn-${exId}-${key}" 
                                onclick="window.checkP2ExampleAnswer('${exId}', '${key}', '${correctAns}')">
                            ${key}
                        </button>
                    `;
                    transcriptChoicesHtml += `
                        <div class="p2-ex-transcript-choice" id="transcript-choice-${exId}-${key}">
                            <span class="lbl">(${key})</span> <span class="txt">${ex.choices[key]}</span>
                        </div>
                    `;
                });
            }
            interactiveButtons += '</div>';
            transcriptChoicesHtml += '</div>';

            html += `
                <div class="p2-ex-card" id="${exId}">
                    ${audioHtml}
                    ${interactiveButtons}
                    
                    <div class="p2-ex-transcript" id="transcript-${exId}" style="display: none;">
                        <div class="p2-ex-question-text">
                            ${(ex.question || '').replace(/^EXAMPLE \d+:\s*/i, '')}
                        </div>
                        ${transcriptChoicesHtml}
                    </div>
                </div>
            `;
        });
        
        examplesContentAreaP2.innerHTML = html;
    }

    if (secBtnTheoryP2) {
        secBtnTheoryP2.addEventListener("click", () => {
            document.querySelectorAll('.panel-section-btn-p2').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.panel-content-p2').forEach(c => c.classList.remove('active'));
            secBtnTheoryP2.classList.add('active');
            if(secTheoryP2) secTheoryP2.classList.add('active');
        });
    }
    
    if (secBtnExamplesP2) {
        secBtnExamplesP2.addEventListener("click", () => {
            document.querySelectorAll('.panel-section-btn-p2').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.panel-content-p2').forEach(c => c.classList.remove('active'));
            secBtnExamplesP2.classList.add('active');
            if(secExamplesP2) secExamplesP2.classList.add('active');
        });
    }

// ================= PART 04 FUNCTIONS =================

    
    function loadSectionP1(sectionId) {
        if (LOCKED_SECTIONS.includes(sectionId) && !window.isUnlocked) {
            window.showPaywallModal(() => loadSectionP1(sectionId));
            return;
        }
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
            <div class="ppt-slide-container">
                <div class="ppt-header">
                    LÝ THUYẾT
                </div>
                <div class="ppt-content" id="p1-slide-content">
                    <!-- Slide content rendered here -->
                </div>
                <div class="ppt-audio-bar" id="p1-slide-audio-bar">
                    <div id="p1-slide-audio-container"></div>
                </div>
                <div class="ppt-nav">
                    <button id="p1-slide-prev" class="ppt-nav-btn">
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg> LÙI LẠI
                    </button>
                    <div style="font-weight: 700; color: #64748b; font-size: 1.05rem; letter-spacing: 0.05em; display: flex; align-items: center;">
                        SLIDE &nbsp;<select id="p1-slide-select" style="padding: 4px 8px; border-radius: 6px; border: 1px solid #cbd5e1; font-weight: bold; color: #0f172a; font-size: 1rem; cursor: pointer; outline: none; background: white; margin: 0 4px;">
                            ${state.part01SlidesData.map((_, i) => `<option value="${i+1}" ${state.part01CurrentSlide === i+1 ? 'selected' : ''}>${i+1}</option>`).join('')}
                        </select>&nbsp; / &nbsp;<span id="p1-slide-total">${state.part01TotalSlides}</span>
                    </div>
                    <button id="p1-slide-next" class="ppt-nav-btn" style="background: linear-gradient(135deg, #2563eb, #1e3a8a); border: none; color: white;">
                        TIẾP TỤC <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6 6 6"/></svg>
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

        document.getElementById("p1-slide-select").addEventListener("change", (e) => {
            state.part01CurrentSlide = parseInt(e.target.value);
            updatePart01SlideView();
        });
    }
    
    function updatePart01SlideView() {
        const slide = state.part01SlidesData[state.part01CurrentSlide - 1];
        if (!slide) return;
        
        const contentContainer = document.getElementById("p1-slide-content");
        const selectEl = document.getElementById("p1-slide-select");
        if (selectEl) selectEl.value = state.part01CurrentSlide;
        
        const prevBtn = document.getElementById("p1-slide-prev");
        const nextBtn = document.getElementById("p1-slide-next");
        
        
        if (slide.practice) {
            const p = slide.practice;
            const imgPath = slide.images && slide.images.length > 0 ? `data/graphics/part01/${slide.images[0]}` : '';
            
            let optionsHtml = '';
            const labels = ['A', 'B', 'C', 'D'];
            p.options.forEach((opt, i) => {
                const isCorrect = labels[i] === p.answer;
                optionsHtml += `
                    <div class="practice-option" data-correct="${isCorrect}" style="display: flex; align-items: flex-start; gap: 8px; padding: 12px 16px; border: 1px solid var(--border); border-radius: 8px; margin-bottom: 12px; cursor: pointer; transition: all 0.2s;" onclick="selectPracticeOption(this)">
                        <strong style="font-size: 1.1em; flex-shrink: 0; min-width: 24px;">${labels[i]}.</strong> <span style="flex: 1;">${opt}</span>
                    </div>
                `;
            });
            
            let vocabHtml = '';
            p.vocab.forEach(v => {
                vocabHtml += `
                    <div style="display: flex; gap: 8px; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px dashed #e2e8f0; font-size: 1.15rem;">
                        <span style="font-weight: 600; color: #0284c7; min-width: 140px; display: inline-block;">${v.en} <span onclick="playTTS(this.dataset.text, event)" data-text="${v.en.replace(/"/g, '&quot;')}" style="cursor: pointer; margin-left: 4px; opacity: 0.5; font-size: 0.9em;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.5'" title="Đọc từ này">🔊</span></span>
                        <span style="color: var(--text-main);">- ${v.vi}</span>
                    </div>
                `;
            });

            const hideRedWordCSS = `
                <style>
                    #practice-options-container:not([data-checked="true"]) .practice-option span[style*="color: #FF0000"] {
                        color: transparent !important;
                        border-bottom: 1px solid #94a3b8;
                    }
                </style>
            `;

            contentContainer.innerHTML = `
                ${hideRedWordCSS}
                <div style="display: flex; flex-direction: row; gap: 40px; flex-wrap: nowrap; align-items: stretch; justify-content: center; width: 100%;">
                    <div style="flex: 1; max-width: 35%; display: flex; justify-content: center; align-items: flex-start;">
                        <img src="${imgPath}" alt="Practice Image" style="width: 100%; max-height: 450px; object-fit: contain; border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.08);">
                    </div>
                    <div style="flex: 1; min-width: 300px; max-width: 65%; font-size: 1.15rem; line-height: 1.6; color: var(--text-main); display: flex; flex-direction: column;">
                        <div id="practice-options-container" style="margin-bottom: 24px;">
                            ${optionsHtml}
                        </div>
                        <div style="display: flex; gap: 16px; margin-bottom: 24px;">
                            <button onclick="checkPracticeAnswer(this)" style="background: #2563eb; color: white; border: none; padding: 12px 32px; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 1.1rem; box-shadow: 0 4px 12px rgba(37,99,235,0.2); transition: all 0.2s;" onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'">KIỂM TRA</button>
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
            let hasImage = slide.images && slide.images.length > 0;

        let isMultipleImages = hasImage && slide.images.length > 1;
        let imgHtml = "";
        
        if (hasImage) {
            let imgFlexDir = isMultipleImages ? "row" : "column";
            let imgGap = isMultipleImages ? "20px" : "0px";
            imgHtml = `<div class="slide-images" style="display: flex; flex-direction: ${imgFlexDir}; gap: ${imgGap}; align-items: center; justify-content: center; background: #f8fafc; border-radius: 12px; padding: 20px; border: 1px solid var(--border); box-shadow: inset 0 2px 10px rgba(0,0,0,0.02);">`;
            slide.images.forEach(img => {
                let imgMargin = isMultipleImages ? "0" : "0 0 8px 0";
                imgHtml += `<img src="data/graphics/part01/${img}" alt="Slide Image" style="max-width: 100%; max-height: 300px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin: ${imgMargin}; flex: 1; min-width: 0;">`;
            });
            imgHtml += `</div>`;
        }

        let isTitleSlide = false;
        if (!hasImage && slide.text.length > 0 && slide.text.length <= 4) {
            const strippedText = slide.text.map(t => t.replace(/<[^>]+>/g, ''));
            const hasLongText = strippedText.some(t => t.length > 60);
            const hasBullets = strippedText.some(t => t.includes('•') || t.includes('Directions:'));
            
            if (!hasLongText && !hasBullets) {
                isTitleSlide = true;
            }
        }
        
        let textHtml = slide.text.map((t, idx) => {
            if (t.trim().startsWith("http") || t.trim().match(/^[a-zA-Z0-9_\-\.]+$/)) {
                return '';
            }
            if (t.includes('class="slide-images"') || t.includes('style=')) {
                // If it already has custom styling or is a complex HTML block, don't wrap it with margin
                return `<div>${t}</div>`;
            }
            if (isTitleSlide) {
                return `<div style="margin-bottom: 24px; text-align: center; font-size: ${idx === 0 ? '2.25rem' : '1.75rem'}; font-weight: 800; line-height: 1.5; text-transform: uppercase;">${t}</div>`;
            }
            return `<div style="margin-bottom: 16px;">${t}</div>`;
        }).join('');
        
        if (hasImage) {
            if (isMultipleImages) {
                // Images horizontally, text below vertically centered
                contentContainer.innerHTML = `
                    <div style="display: flex; flex-direction: column; gap: 24px; width: 100%; align-items: center;">
                        ${imgHtml}
                        <div class="slide-text" style="font-size: 1.15rem; line-height: 1.8; color: var(--text-main); display: flex; flex-direction: column; align-items: center; text-align: center;">
                            ${textHtml}
                        </div>
                    </div>
                `;
            } else {
                // Single image: left/right layout
                contentContainer.innerHTML = `
                    <div style="display: flex; flex-direction: row; gap: 32px; flex-wrap: wrap; align-items: center;">
                        <div style="flex: 1.2; min-width: 300px; display: flex; justify-content: center;">
                            ${imgHtml}
                        </div>
                        <div class="slide-text" style="flex: 1; min-width: 300px; font-size: 1.35rem; line-height: 2; color: var(--text-main); display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
                            ${textHtml}
                        </div>
                    </div>
                `;
            }
        } else {
            let containerStyle = isTitleSlide 
                ? `display: flex; flex-direction: column; justify-content: center; align-items: center; width: 100%; height: 100%;`
                : `display: flex; flex-direction: column; justify-content: center; align-items: flex-start; width: 100%; height: 100%;`;
                
            contentContainer.innerHTML = `
                <div style="${containerStyle}">
                    ${textHtml}
                </div>
            `;
        }
        
                }

        prevBtn.style.opacity = state.part01CurrentSlide === 1 ? "0.4" : "1";
        prevBtn.style.cursor = state.part01CurrentSlide === 1 ? "not-allowed" : "pointer";
        nextBtn.style.opacity = state.part01CurrentSlide === state.part01TotalSlides ? "0.4" : "1";
        nextBtn.style.cursor = state.part01CurrentSlide === state.part01TotalSlides ? "not-allowed" : "pointer";
        
        const audioBar = document.getElementById("p1-slide-audio-bar");
        const audioContainer = document.getElementById("p1-slide-audio-container");
        audioContainer.innerHTML = '';
        if (slide.audio) {
            audioBar.style.display = "block";
            createAudioPlayer(slide.audio, audioContainer);
        } else {
            audioBar.style.display = "none";
        }
    }

    
    function renderTestP1(testData, container) {
        if (!testData.practice_sets || testData.practice_sets.length === 0) {
            container.innerHTML = "<p>Đề thi đang được cập nhật...</p>";
            return;
        }

        if (!window.checkP1TestAnswer) {
            window.checkP1TestAnswer = function(globalQId, selectedKey, correctKey) {
                const card = document.getElementById(`p1-test-card-${globalQId}`);
                if (!card) return;
                
                const btns = card.querySelectorAll('.p1-interactive-btn');
                btns.forEach(btn => {
                    btn.style.pointerEvents = 'none';
                    if (btn.id === `btn-${globalQId}-${correctKey}`) {
                        btn.classList.add('correct');
                    } else if (btn.id === `btn-${globalQId}-${selectedKey}` && selectedKey !== correctKey) {
                        btn.classList.add('incorrect');
                    }
                });
                
                const transcript = card.querySelector('.p1-ex-transcript');
                if (transcript) {
                    transcript.style.display = 'block';
                    transcript.style.animation = 'fadeIn 0.5s ease forwards';
                }
                
                const correctChoice = document.getElementById(`transcript-choice-${globalQId}-${correctKey}`);
                if (correctChoice) correctChoice.classList.add('highlight-correct');
                
                // Save progress
                state.answeredQuestions[globalQId] = selectedKey;
                try {
                    localStorage.setItem("toeic_answered_questions", JSON.stringify(state.answeredQuestions));
                } catch(e) {}
                updateRouteProgress();
            };
        }

        let html = `
            <style>
                @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
                .p1-ex-card {
                    background: var(--bg-card); border: 1px solid rgba(255,255,255,0.08); padding: 30px; border-radius: 24px;
                    margin-bottom: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); transition: all 0.4s ease;
                    backdrop-filter: blur(10px); display: flex; flex-direction: column; align-items: center;
                }
                .p1-ex-card:hover { border-color: rgba(99, 102, 241, 0.4); box-shadow: 0 15px 35px rgba(0,0,0,0.15); }
                
                .p1-image-container { width: 100%; max-width: 500px; margin-bottom: 25px; border-radius: 12px; overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
                .p1-image-container img { width: 100%; height: auto; display: block; object-fit: cover; }
                
                .p1-audio-player { text-align: center; margin-bottom: 25px; width: 100%; }
                
                .p1-interactive-buttons { display: flex; justify-content: center; gap: 20px; margin-bottom: 10px; flex-wrap: wrap; }
                .p1-interactive-btn {
                    background: rgba(255,255,255,0.03); border: 2px solid rgba(255,255,255,0.15); color: var(--text-main);
                    width: 65px; height: 65px; border-radius: 50%; font-size: 1.25rem; font-weight: 800;
                    cursor: pointer; transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
                    display: flex; align-items: center; justify-content: center; outline: none;
                }
                .p1-interactive-btn:hover { background: rgba(99, 102, 241, 0.1); border-color: #6366f1; transform: scale(1.1); color: #818cf8; }
                .p1-interactive-btn.correct { background: #16a34a; border-color: #15803d; color: white; transform: scale(1.1); box-shadow: 0 0 15px rgba(22, 163, 74, 0.5); }
                .p1-interactive-btn.incorrect { background: #dc2626; border-color: #b91c1c; color: white; transform: scale(0.95); opacity: 0.8; }
                
                .p1-ex-transcript {
                    margin-top: 25px; padding-top: 25px; border-top: 1px dashed rgba(255,255,255,0.15); width: 100%;
                }
                .p1-ex-transcript-choices { display: flex; flex-direction: column; gap: 10px; }
                .p1-ex-transcript-choice {
                    display: flex; gap: 15px; font-size: 1.1rem; color: var(--text-muted); padding: 12px 18px;
                    border-radius: 12px; background: var(--border); transition: all 0.3s ease; border: 1px solid transparent;
                }
                .p1-ex-transcript-choice .lbl { font-weight: 900; color: #94a3b8; min-width: 25px; }
                .p1-ex-transcript-choice.highlight-correct {
                    background: rgba(34, 197, 94, 0.1); color: #4ade80; border-color: rgba(34, 197, 94, 0.3);
                }
                .p1-ex-transcript-choice.highlight-correct .lbl { color: #4ade80; }
            </style>
            
            <div class="p2-hero" style="background: radial-gradient(circle at 0% 0%, rgba(99, 102, 241, 0.15) 0%, transparent 50%), linear-gradient(145deg, #0f172a 0%, #020617 100%); margin-bottom: 30px; padding: 24px; border-radius: 16px; color: #f8fafc;">
                <h2 class="p2-hero-title" style="text-align: center; font-weight: 800; font-size: 1.5rem; margin-bottom: 8px; color: #f8fafc;">LUYỆN TẬP TƯƠNG TÁC: ${testData.title}</h2>
                <p class="p2-hero-subtitle" style="text-align: center; color: #94a3b8;">Bấm PLAY để nghe Audio. Chọn đáp án A, B, C, D để hiện nội dung chi tiết.</p>
            </div>
            <div class="practice-sets-container" style="display: flex; flex-direction: column; gap: 20px;">
        `;
        
        testData.practice_sets.forEach((set, setIndex) => {
            const q = set.questions[0]; 
            if (!q) return;
            
            const qId = q.id;
            const globalQId = `p1_${testData.id}_q_${qId}`;
            const correctAns = q.answer || 'A';
            const savedAns = state.answeredQuestions[globalQId] || null;
            
            // Image path: since set.image is already "part01/ets2025/...", we prepend "media/"
            const imageHtml = set.image ? `
                <div class="p1-image-container">
                    <img src="media/${set.image}" alt="Question ${qId}" onerror="this.src='data/graphics/part01/${set.image}'">
                </div>
            ` : '';
            
            const audioHtml = set.audio ? `
                <div class="p1-audio-player">
                    <audio id="audio-${globalQId}" src="media/${set.audio}" controls style="width: 100%; max-width: 400px; border-radius: 50px; outline: none;"></audio>
                </div>
            ` : `<div class="p1-audio-player"><p style="color:#ef4444;">[Thiếu Audio]</p></div>`;
            
            let interactiveButtons = '<div class="p1-interactive-buttons">';
            let transcriptChoicesHtml = '<div class="p1-ex-transcript-choices">';
            
            if (q.choices) {
                ['A', 'B', 'C', 'D'].forEach(key => {
                    const choiceText = q.choices[key] || "";
                    let btnClass = "p1-interactive-btn";
                    
                    if (savedAns) {
                        btnClass += " disabled";
                        if (key === correctAns) btnClass += " correct";
                        else if (key === savedAns) btnClass += " incorrect";
                    }
                    
                    const pointerEvents = savedAns ? "pointer-events: none;" : "";
                    
                    interactiveButtons += `
                        <button class="${btnClass}" id="btn-${globalQId}-${key}" style="${pointerEvents}"
                                onclick="window.checkP1TestAnswer('${globalQId}', '${key}', '${correctAns}')">
                            ${key}
                        </button>
                    `;
                    
                    let highlightClass = (savedAns && key === correctAns) ? "highlight-correct" : "";
                    const vietText = (q.vietnamese_choices && q.vietnamese_choices[key]) ? q.vietnamese_choices[key] : "";
                    const vietHtml = vietText ? `<br><span style="font-style: italic; color: var(--color-purple); font-size: 0.95rem;">${vietText}</span>` : "";
                    
                    transcriptChoicesHtml += `
                        <div class="p1-ex-transcript-choice ${highlightClass}" id="transcript-choice-${globalQId}-${key}">
                            <span class="lbl">(${key})</span> <span class="txt">${choiceText}${vietHtml}</span>
                        </div>
                    `;
                });
            }
            interactiveButtons += '</div>';
            transcriptChoicesHtml += '</div>';

            let vocabHtml = '';
            if (q.vocabulary && q.vocabulary.length > 0) {
                let vocabItems = q.vocabulary.map(v => `
                    <div style="margin-bottom: 8px; font-size: 1.05rem;">
                        <span style="font-weight: 700; color: #0284c7;">${v.pos === 'v' && v.base && v.gerund && v.base !== v.gerund ? `${v.base} ➔ ${v.gerund}` : v.en}</span> 
                        <span style="color: #64748b; font-size: 0.9em; font-family: monospace;">${v.ipa}</span>
                        <span style="color: #a855f7; font-size: 0.9em; font-style: italic;">(${v.pos})</span>: 
                        <span style="color: var(--text-main);">${v.vi}</span>
                        <span onclick="playTTS(this.dataset.text, event)" data-text="${(v.pos === 'v' && v.base && v.gerund && v.base !== v.gerund ? v.base + ', ' + v.gerund : (v.base || v.en)).replace(/"/g, '&quot;')}" style="cursor: pointer; margin-left: 6px; opacity: 0.6; font-size: 1.1em;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.6'" title="Đọc từ này">🔊</span>
                    </div>
                `).join('');
                vocabHtml = `
                    <div class="p1-vocab-box" style="margin-top: 20px; padding: 18px 20px; border-radius: 12px; background: var(--bg-sidebar); border: 1px solid var(--border); box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);">
                        <h4 style="font-weight: 800; font-size: 1.1rem; color: #10b981; margin-bottom: 15px; display: flex; align-items: center; gap: 8px; text-transform: uppercase;">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>
                            Từ vựng hữu ích
                        </h4>
                        ${vocabItems}
                    </div>
                `;
            }
            
            html += `
                <div class="p1-ex-card" id="p1-test-card-${globalQId}">
                    <h3 style="align-self: flex-start; margin-bottom: 20px; font-weight: 800; color: var(--text-main);">QUESTION ${qId}</h3>
                    ${imageHtml}
                    ${audioHtml}
                    ${interactiveButtons}
                    
                    <div class="p1-ex-transcript" id="transcript-${globalQId}" style="display: ${savedAns ? 'block' : 'none'};">
                        ${transcriptChoicesHtml}
                        ${vocabHtml}
                    </div>
                </div>
            `;
        });
        
        html += `</div>`;
        container.innerHTML = html;
    }


    function loadSectionP4(id) {
        const isUnlocked = window.isUnlocked;
        if (LOCKED_SECTIONS.includes(id) && !isUnlocked) {
            window.showPaywallModal(() => loadSection(id));
            return;
            if (false) {
                sessionStorage.setItem("portal_unlocked_v2", "true");
                alert("Mở khóa thành công!");
                initializePart03Sidebar();
    initializePart01Sidebar();
    if (typeof initializePart02Sidebar === 'function') initializePart02Sidebar();
    initializePart04Sidebar(); // Refresh sidebar to remove locks
            } else {
                if (pass !== null) {
                    alert("Mật khẩu không chính xác!");
                }
                // Fallback to active section or overview
                const fallbackId = state.part04ActiveSection && state.part04ActiveSection !== id ? state.part04ActiveSection : "overview";
                document.querySelectorAll(".submenu-item").forEach(item => {
                    if (item.getAttribute("data-id") === fallbackId) {
                        item.classList.add("active");
                    } else {
                        item.classList.remove("active");
                    }
                });
                return;
            }
        }
        
        state.part04ActiveSection = id;
        
        if (state.activeView !== "part4") {
            switchView("part4");
        }
        
        document.querySelectorAll(".submenu-item").forEach(item => {
            if (item.getAttribute("data-id") === id) {
                item.classList.add("active");
            } else {
                item.classList.remove("active");
            }
        });
        
        const isGeneral = id === "overview" || id === "tips";
        const panelSectionsBar = document.getElementById("panel-sections-bar");
        if (panelSectionsBar) {
            panelSectionsBar.style.display = isGeneral ? "none" : "flex";
        }
        
        const section = state.part04Data.find(item => item.id === id);
        if (!section) return;
        
        // Override section title using category tree mapping
        let displayTitle = section.title;
        let parentText = "Lý thuyết chung";
        
        let foundNode = null;
        categoryTree.forEach(node => {
            if (node.type === "item" && node.id === id) {
                foundNode = node;
                parentText = "Tổng quan";
            } else if (node.type === "group") {
                const match = node.items.find(item => item.id === id);
                if (match) {
                    foundNode = match;
                    parentText = node.title;
                }
            }
        });
        
        if (foundNode) {
            displayTitle = foundNode.title;
        } else if (section.type === "topic" || section.type === "test") {
            parentText = "Luyện tập ETS 2026";
            displayTitle = section.title;
        }
        
        breadParentP4.textContent = parentText;
        breadCurrentP4.textContent = displayTitle;
        panelTitleP4.textContent = displayTitle;
        
        const hasTheory = section.theory && section.theory.length > 0;
        const theoryTabBtn = document.getElementById("sec-btn-theory-p4");
        if (theoryTabBtn) {
            if (hasTheory) {
                theoryTabBtn.classList.remove("hidden");
            } else {
                theoryTabBtn.classList.add("hidden");
            }
        }

        const hasVocabulary = section.vocabulary && section.vocabulary.length > 0;
        const vocabularyTabBtn = document.getElementById("sec-btn-vocabulary");
        if (vocabularyTabBtn) {
            if (hasVocabulary) {
                vocabularyTabBtn.classList.remove("hidden");
            } else {
                vocabularyTabBtn.classList.add("hidden");
            }
        }

        const hasExamples = section.examples && section.examples.length > 0;
        const examplesTabBtn = document.getElementById("sec-btn-examples");
        if (examplesTabBtn) {
            if (hasExamples) {
                examplesTabBtn.classList.remove("hidden");
            } else {
                examplesTabBtn.classList.add("hidden");
            }
        }

        const hasPractice = (section.practice && section.practice.length > 0) || (section.practice_sets && section.practice_sets.length > 0);
        const practiceTabBtn = document.getElementById("sec-btn-practice");
        if (practiceTabBtn) {
            if (hasPractice) {
                practiceTabBtn.classList.remove("hidden");
            } else {
                practiceTabBtn.classList.add("hidden");
            }
        }

        // Auto-switch to the first tab that has content
        let targetTab = "theory";
        if (section.theory && section.theory.length > 0) {
            targetTab = "theory";
        } else if (section.vocabulary && section.vocabulary.length > 0) {
            targetTab = "vocabulary";
        } else if (section.examples && section.examples.length > 0) {
            targetTab = "examples";
        } else if ((section.practice && section.practice.length > 0) || (section.practice_sets && section.practice_sets.length > 0)) {
            targetTab = "practice";
        }
        state.part04ActiveTab = targetTab;
        
        renderPanelTabP4(state.part04ActiveTab);
    }
    
    panelTabBtnsP4.forEach(btn => {
        btn.addEventListener("click", () => {
            const sec = btn.getAttribute("data-section");
            state.part04ActiveTab = sec;
            renderPanelTabP4(sec);
        });
    });

    function renderPanelTabP4(tabName) {
        stopAudio();
        
        panelTabsP4.forEach(tab => {
            if (tab.id === `sec-${tabName}-p4`) {
                tab.classList.add("active");
            } else {
                tab.classList.remove("active");
            }
        });
        
        panelTabBtnsP4.forEach(b => {
            if (b.getAttribute("data-section") === tabName) {
                b.classList.add("active");
            } else {
                b.classList.remove("active");
            }
        });
        
        const section = state.part04Data.find(item => item.id === state.part04ActiveSection);
        if (!section) return;
        
        if (tabName === "theory") {
            renderTheoryP4(section);
        } else if (tabName === "vocabulary") {
            renderVocabularyP4(section);
        } else if (tabName === "examples") {
            renderExamplesP4(section);
        } else if (tabName === "practice") {
            renderPracticeP4(section);
        }
    }

    /* -------------------------------------------------------------
       5.5 TRANSLATION HTML BUILDERS
       ------------------------------------------------------------- */
    function renderQuestionTextHtml(q, idLabel, textPrefix = "") {
        let qText = q.question;
        if (qText) {
            qText = qText.replace(/^(?:<[^>]*>|\s)*Question\s*\d+[\.\:]?(?:<\/[^>]*>|\s)*/i, "");
            if (qText.includes("PRACTICE") || qText.includes("Example") || qText.includes("EXAMPLE")) {
                textPrefix = "";
            }
        }
        const qViet = q.vietnamese_question || "";
        
        let graphicHtml = "";
        const lowerQText = (qText || "").toLowerCase();
        const lowerQViet = (qViet || "").toLowerCase();
        const isVisual = lowerQText.includes("look at the graphic") || 
                         lowerQText.includes("look at the map") ||
                         lowerQText.includes("look at the schedule") ||
                         lowerQText.includes("look at the chart") ||
                         lowerQText.includes("look at the diagram") ||
                         lowerQViet.includes("quan sát hình") ||
                         lowerQViet.includes("nhìn vào hình") ||
                         lowerQViet.includes("quan sát sơ đồ") ||
                         lowerQViet.includes("nhìn vào sơ đồ");
                         
        if (isVisual) {
            const CROPPED_GRAPHICS_P4 = {
                27: "data/graphics/part04/practice2_q2.png"
            };
            let imgSrc = `../TOEIC PART 04/Slide${q.slide_index}.png`;
            if (CROPPED_GRAPHICS_P4[q.slide_index]) {
                imgSrc = CROPPED_GRAPHICS_P4[q.slide_index];
            }
            graphicHtml = `
                <div class="visual-graphic-container" style="margin: 16px 0; text-align: center; width: 100%;">
                    <img class="visual-graphic-img" 
                         src="${imgSrc}" 
                         onerror="this.onerror=null; this.src='../TOEIC PART 04/Slide${q.slide_index}.png';"
                         style="max-width: 100%; max-height: 450px; border: 2px solid var(--border); border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); display: block; margin: 0 auto;" 
                         alt="Look at the graphic (Slide ${q.slide_index})">
                </div>
            `;
        }

        if (!qViet) {
            return `
                <div class="question-text" style="font-size: 1.25rem; font-weight: 700; line-height: 1.5; color: var(--text-main); margin-bottom: 16px;">${textPrefix}${qText}</div>
                ${graphicHtml}
            `;
        }
        
        return `
            <div class="question-text-wrapper" style="cursor: pointer; width: 100%;" onclick="const t = this.querySelector('.q-trans'); t.style.display = t.style.display === 'block' ? 'none' : 'block'; event.stopPropagation();" title="Click vào câu hỏi để xem dịch nghĩa">
                <div class="question-text" style="margin-bottom: 16px; text-align: left; width: 100%; font-size: 1.25rem; font-weight: 700; line-height: 1.5; color: var(--text-main);">
                    ${textPrefix}${qText}
                </div>
                <div class="q-trans" style="display: none;">
                    ${qViet}
                </div>
            </div>
            ${graphicHtml}
        `;
    }

    function renderChoicesHtml(q, isReview = false, userAnswer = null) {
        let choicesHtml = "";
        Object.keys(q.choices).forEach(key => {
            const optText = q.choices[key];
            const optViet = q.vietnamese_choices ? q.vietnamese_choices[key] : "";
            
            let extraClass = "";
            if (isReview) {
                extraClass = "checked-done";
                if (key === q.answer) {
                    extraClass += " correct";
                } else if (key === userAnswer) {
                    extraClass += " incorrect";
                }
            }
            
            let transDiv = "";
            if (optViet) {
                transDiv = `
                    <div class="c-trans" style="display: none; color: var(--color-purple); font-size: 0.88rem; font-style: italic; margin-top: 6px; text-align: left; width: 100%; border-left: 2px solid var(--color-purple); padding-left: 8px; line-height: 1.4; font-weight: 500;">
                        ${optViet}
                    </div>
                `;
            }
            
            choicesHtml += `
                <button class="choice-option ${extraClass}" data-key="${key}" data-slide="${q.slide_index}" data-q-slide="${q.slide_index}" style="display: flex; flex-direction: column; align-items: flex-start; padding: 16px 20px; width: 100%; border-radius: 8px !important; margin-bottom: 12px; background: #fff; box-shadow: 0 2px 6px rgba(0,0,0,0.03); border: 1px solid var(--border); transition: all 0.2s;">
                    <div style="display: flex; align-items: center; width: 100%;">
                        <div class="choice-radio-circle" style="width: 24px; height: 24px; margin-right: 16px;"></div>
                        <div class="choice-letter" style="margin-right: 16px; flex-shrink: 0; font-size: 1.15rem; font-weight: 800;">${key}</div>
                        <div class="choice-text" style="flex: 1; text-align: left; font-weight: 600; font-size: 1.15rem; color: var(--text-main); line-height: 1.4;">${optText}</div>
                    </div>
                    ${transDiv}
                </button>
            `;
        });
        return choicesHtml;
    }

    function renderTranscriptHtml(transcriptList, vietTranscriptList) {
        let html = "";
        transcriptList.forEach((line, idx) => {
            const lineViet = vietTranscriptList && vietTranscriptList[idx] ? vietTranscriptList[idx] : "";
            let transHtml = "";
            if (lineViet) {
                const cleanViet = lineViet.replace(/^[A-Za-z0-9]+[-A-Za-z0-9]*\s*:\s*/, "");
                const highlightedViet = cleanViet.replace(/(\(\d+\)[^.?!]*(?:[.?!]|$))/g, '<strong style="color: #ff3333; font-style: italic;">$1</strong>');
                transHtml = `<div class="line-trans-text" style="color: var(--text-muted); font-size: 0.88rem; font-style: italic; margin-top: 4px; border-left: 2px solid var(--border); padding-left: 8px;">${highlightedViet}</div>`;
            }
            let formattedLine = line.replace(/(\(\d+\)[^.?!]*(?:[.?!]|$))/g, '<strong style="color: #ff3333; font-style: italic;">$1</strong>');
            formattedLine = formattedLine.replace(/^([A-Za-z0-9]+[-A-Za-z0-9]*\s*:\s*)/, '<strong style="color: var(--color-blue);">$1</strong>');
            html += `
                <div class="transcript-line-wrapper" style="margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px dashed var(--border); text-align: left;">
                    <p class="transcript-line" style="margin: 0; font-weight: 500; line-height: 1.6; font-size: 1.15rem;">${formattedLine}</p>
                    ${transHtml}
                </div>
            `;
        });
        return html;
    }

    function renderScriptCardHtml(idLabel, transcriptHtml, explanationHtml) {
        return `
            <div class="reveal-script-card hidden" id="reveal-card-${idLabel}">
                <div class="reveal-header" id="header-reveal-${idLabel}">
                    <span><strong>📄 TRANSCRIPT & GIẢI THÍCH ĐÁP ÁN</strong></span>
                    ${icons.chevronDown}
                </div>
                <div class="reveal-content" id="reveal-content-${idLabel}" style="padding: 20px; text-align: left;">
                    ${explanationHtml}
                    <h4 style="margin: 20px 0 10px 0; font-size: 1rem; font-weight: 800; text-transform: uppercase; color: var(--color-purple); display: flex; align-items: center; gap: 8px; border-bottom: 1px solid var(--border); padding-bottom: 8px;">
                        🎤 TRANSCRIPT BÀI NGHE
                    </h4>
                    ${transcriptHtml}
                </div>
            </div>
        `;
    }

    function hookScriptCardToggler(idLabel) {
        setTimeout(() => {
            const revHeader = document.getElementById(`header-reveal-${idLabel}`);
            const revContent = document.getElementById(`reveal-content-${idLabel}`);
            if (revHeader && revContent) {
                revHeader.addEventListener("click", () => {
                    revContent.classList.toggle("open");
                    const svg = revHeader.querySelector("svg");
                    if (svg) {
                        if (revContent.classList.contains("open")) {
                            svg.outerHTML = icons.chevronUp;
                        } else {
                            svg.outerHTML = icons.chevronDown;
                        }
                    }
                });
            }
        }, 50);
    }

    /* -------------------------------------------------------------
       6. RENDERING DETAILS (THEORY, VOCABULARY, EXAMPLES, PRACTICE)
       ------------------------------------------------------------- */
    
    // A. THEORY
    function renderTheoryP4(section) {
        theoryContentAreaP4.innerHTML = "";
        theoryContentAreaP4.style.maxWidth = "1000px";
        theoryContentAreaP4.style.margin = "0 auto";
        
        if (!section.theory || section.theory.length === 0) {
            theoryContentAreaP4.innerHTML = "<p style='color: var(--text-muted); font-weight: 700;'>Không có lý thuyết cho phần này.</p>";
            return;
        }
        
        // Custom interactive landing page for Section Overview (Inspired by Speaking website design elements)
        if (section.id === "overview") {
            theoryContentAreaP4.innerHTML = `
                <div class="overview-hero-p3">
                    <div class="overview-tag">
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                        Part 04: Short Talks
                    </div>
                    <h2 class="overview-title">TỔNG QUAN NỘI DUNG PHẦN 04</h2>
                    <p class="overview-desc">Học cách nghe hiểu các bài nói chuyện ngắn, nắm bắt từ khóa và phản xạ chọn đáp án nhanh chóng trong bài nghe.</p>
                    
                    <div class="stats-container">
                        <div class="stat-card">
                            <div class="stat-icon"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div>
                            <div class="stat-info">
                                <strong>30 Câu Hỏi</strong>
                                <span>Từ câu 71 đến câu 100</span>
                            </div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-icon"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></div>
                            <div class="stat-info">
                                <strong>10 Bài Nói</strong>
                                <span>Bài nói chuyện ngắn</span>
                            </div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-icon"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></div>
                            <div class="stat-info">
                                <strong>1 Người</strong>
                                <span>Số lượng người nói</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="rules-header">
                    <svg viewBox="0 0 24 24" width="32" height="32" fill="none" stroke="#6366f1" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="9" y1="9" x2="15" y2="9"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="15" y2="17"/></svg> 
                    <span>CẤU TRÚC VÀ CÁC QUY TẮC TRỌNG TÂM</span>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px; margin-bottom: 40px;">
                    <div class="rule-card">
                        <div class="rule-icon"><svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></div>
                        <h4>10 Bài Nói</h4>
                        <p>Mỗi bài nói chuyện ngắn gồm 03 câu hỏi đi kèm. Nội dung thường xoay quanh các thông báo trong công việc, tin tức, diễn văn, và đời sống hàng ngày...</p>
                    </div>
                    <div class="rule-card">
                        <div class="rule-icon"><svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a5 5 0 0 0-5 5v3.18a3 3 0 0 0-.58 1.7l1 5A3 3 0 0 0 10.38 18h3.24a3 3 0 0 0 3-2.12l1-5a3 3 0 0 0-.58-1.7V6a5 5 0 0 0-5-5z"/></svg></div>
                        <h4>Chỉ Được Nghe 1 Lần</h4>
                        <p>Thí sinh không được nghe lại lần thứ hai. Hãy tập trung cao độ ngay khi âm thanh bắt đầu phát và không phân tâm khi bỏ lỡ từ khóa.</p>
                    </div>
                    <div class="rule-card">
                        <div class="rule-icon"><svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div>
                        <h4>Tận Dụng Thời Gian Chờ</h4>
                        <p>Trong khi băng đọc câu hỏi, hãy tranh thủ đánh dấu đáp án và <strong>đọc trước bộ câu hỏi tiếp theo</strong> để dự đoán nội dung bài nói sắp nghe.</p>
                    </div>
                </div>
            `;
            return;
        }
        
        const docContainer = document.createElement("div");
        docContainer.className = "theory-document";
        docContainer.style.background = "var(--bg-card)";
        docContainer.style.border = "1px solid var(--border)";
        docContainer.style.padding = "35px 40px";
        docContainer.style.color = "var(--text-main)";
        docContainer.style.lineHeight = "1.75";
        docContainer.style.textAlign = "left";
        
        let docHtml = "";
        
        section.theory.forEach((slide, sIdx) => {
            const lines = slide.text;
            if (!lines || lines.length === 0) return;
            
            const firstLine = lines[0].trim();
            const restLines = lines.slice(1);
            
            // Clean HTML tags to evaluate textual structure
            const cleanFirst = firstLine.replace(/<[^>]*>/g, "").trim();
            
            // Evaluates if the line acts as a divider or main section header
            const isMainHeader = cleanFirst.toUpperCase() === cleanFirst || /^\d+\.\s+/.test(cleanFirst) || cleanFirst.includes("CÂU HỎI") || cleanFirst.includes("LƯU Ý");
            
            if (isMainHeader) {
                // If it's a section header, draw a horizontal spacer above it (except for the first one)
                if (sIdx > 0) {
                    docHtml += `<hr style="border: none; border-top: 1px solid var(--border); margin: 40px 0 30px 0;">`;
                }
                
                docHtml += `
                    <h3 style="font-size: 1.35rem; font-weight: 700; color: var(--color-blue); margin: 0 0 24px 0; text-transform: uppercase; border-left: 4px solid var(--color-purple); padding-left: 14px; line-height: 1.4;">
                        ${firstLine}
                    </h3>
                `;
            } else {
                docHtml += `
                    <p style="font-size: 1.08rem; line-height: 1.7; color: var(--text-main); margin: 0 0 16px 0;">
                        ${firstLine}
                    </p>
                `;
            }
            
            restLines.forEach(line => {
                let cleanLine = line.trim();
                if (!cleanLine) return;
                
                // Match bullets, potentially preceded by leading HTML tags (e.g. <em>, <strong>)
                const htmlBulletRegex = /^((?:<[^>]+>\s*)*)(•|o|-|\*|◦)\s+/i;
                
                const bulletMatch = cleanLine.match(htmlBulletRegex);
                if (bulletMatch) {
                    const bulletChar = bulletMatch[2];
                    const cleanedHtml = cleanLine.replace(htmlBulletRegex, "$1").trim();
                    const isExample = bulletChar === "o" || bulletChar === "-";
                    const bulletClass = isExample ? "theory-bullet example-bullet" : "theory-bullet main-bullet";
                    
                    docHtml += `
                        <div class="${bulletClass}" style="margin-bottom: 12px;">
                            <span>${cleanedHtml}</span>
                        </div>
                    `;
                } else {
                    const rawText = cleanLine.replace(/<[^>]*>/g, "").trim();
                    const isSubHeader = ((cleanLine.startsWith("<strong>") && cleanLine.endsWith("</strong>")) || /^\d+(\.\d+)*\./.test(rawText)) && rawText.length < 120;
                    if (isSubHeader) {
                        docHtml += `
                            <h4 style="font-size: 1.15rem; font-weight: 700; color: var(--text-main); margin: 24px 0 12px 0; line-height: 1.4;">
                                ${cleanLine}
                            </h4>
                        `;
                    } else {
                        docHtml += `
                            <p style="font-size: 1.08rem; line-height: 1.7; color: var(--text-main); margin: 0 0 14px 0;">
                                ${cleanLine}
                            </p>
                        `;
                    }
                }
            });
        });
        
        docContainer.innerHTML = docHtml;
        theoryContentAreaP4.appendChild(docContainer);
    }
     
    // B. VOCABULARY
    function renderVocabularyP4(section) {
        vocabularyContentAreaP4.innerHTML = "";
        vocabularyContentAreaP4.style.maxWidth = "1000px";
        vocabularyContentAreaP4.style.margin = "0 auto";
        
        if (!section.vocabulary || section.vocabulary.length === 0) {
            vocabularyContentAreaP4.innerHTML = "<p style='color: var(--text-muted); font-weight: 700;'>Không có từ vựng cho phần này.</p>";
            return;
        }
        
        section.vocabulary.forEach(slide => {
            const card = document.createElement("div");
            card.className = "vocabulary-card";
            
            const titleText = slide.text[0] || "Từ Vựng";
            const subtitleText = slide.text.length > 1 ? slide.text[1] : "";
            const bullets = slide.text.slice(2);
            
            let bulletsHtml = "";
            bullets.forEach(b => {
                let cleanB = b.trim();
                cleanB = cleanB.replace(/^(o|•|-|\*)\s+/, "");
                bulletsHtml += `
                    <li class="vocabulary-bullet">
                        <span>${cleanB}</span>
                    </li>
                `;
            });
            
            let subtitleHtml = "";
            if (subtitleText) {
                subtitleHtml = `<div class="vocabulary-card-subtitle">${subtitleText}</div>`;
            }
            
            card.innerHTML = `
                <div class="vocabulary-card-header">
                    <span class="vocabulary-card-title">${titleText}</span>
                    <span class="slide-num-tag">Slide ${slide.slide_index}</span>
                </div>
                ${subtitleHtml}
                <ul class="vocabulary-bullet-list">
                    ${bulletsHtml || `<li class="vocabulary-bullet"><span>${titleText}</span></li>`}
                </ul>
            `;
            
            vocabularyContentAreaP4.appendChild(card);
        });
    }
    
    // C. EXAMPLES
    function renderExamplesP4(section) {
        examplesContentAreaP4.innerHTML = "";
        examplesContentAreaP4.style.maxWidth = "1000px";
        examplesContentAreaP4.style.margin = "0 auto";
        
        if (!section.examples || section.examples.length === 0) {
            examplesContentAreaP4.innerHTML = "<p style='color: var(--text-muted); font-weight: 700;'>Không có câu hỏi ví dụ.</p>";
            return;
        }
        
        if (section.type === "topic" || section.type === "test") {
            // Render example sets for topics
            section.examples.forEach((set, setIdx) => {
                const setWrapper = document.createElement("div");
                setWrapper.className = "practice-set-card";
                setWrapper.style.padding = "32px";
                setWrapper.style.marginBottom = "32px";
                setWrapper.style.border = "1px solid var(--border)";
                setWrapper.style.background = "rgba(255, 255, 255, 0.02)";
                setWrapper.style.borderRadius = "12px";
                setWrapper.style.boxShadow = "0 8px 24px rgba(0,0,0,0.04)";
                
                const setHeader = document.createElement("h3");
                setHeader.style.fontSize = "1.1rem";
                setHeader.style.marginBottom = "16px";
                setHeader.style.fontWeight = "800";
                setHeader.textContent = `VÍ DỤ MINH HỌA: ĐOẠN HỘI THOẠI ${set.set_index}`;
                setWrapper.appendChild(setHeader);
                
                const audioDiv = document.createElement("div");
                setWrapper.appendChild(audioDiv);
                createAudioPlayer(set.audio, audioDiv);
                
                const qListDiv = document.createElement("div");
                setWrapper.appendChild(qListDiv);
                
                const userSelections = {};
                const submitBtn = document.createElement("button");
                submitBtn.className = "btn btn-primary";
                submitBtn.style.margin = "20px 0";
                submitBtn.style.padding = "12px 24px";
                submitBtn.style.fontWeight = "700";
                submitBtn.style.borderRadius = "0px !important";
                submitBtn.textContent = "KIỂM TRA";
                submitBtn.disabled = true;

                set.questions.forEach(q => {
                    const qCard = document.createElement("div");
                    qCard.className = "question-block";
                    qCard.style.padding = "20px";
                    qCard.style.marginTop = "16px";
                    
                    const choicesHtml = renderChoicesHtml(q, false);
                    const questionTextHtml = renderQuestionTextHtml(q, `exset-q-${q.slide_index}`, `<strong>QUESTION ${q.id}:</strong> `);
                    
                    qCard.innerHTML = `
                        ${questionTextHtml}
                        <div class="choices-stack" style="margin-top: 12px;">
                            ${choicesHtml}
                        </div>
                    `;
                    
                    qListDiv.appendChild(qCard);
                    
                    const options = qCard.querySelectorAll(".choice-option");
                    options.forEach(opt => {
                        opt.addEventListener("click", () => {
                            if (opt.classList.contains("checked-done")) {
                                const t = opt.querySelector(".c-trans");
                                if (t) t.style.display = t.style.display === "block" ? "none" : "block";
                                return;
                            }
                            
                            // Toggle translation inline on click
                            const t = opt.querySelector(".c-trans");
                            if (t) t.style.display = t.style.display === "block" ? "none" : "block";
                            
                            const key = opt.getAttribute("data-key");
                            userSelections[q.slide_index] = key;
                            
                            options.forEach(o => o.classList.remove("selected"));
                            opt.classList.add("selected");
                            
                            let allSelected = true;
                            set.questions.forEach(qi => {
                                if (!userSelections[qi.slide_index]) {
                                    allSelected = false;
                                }
                            });
                            submitBtn.disabled = !allSelected;
                        });
                    });
                });
                
                setWrapper.appendChild(submitBtn);
                
                // Aggregate explanations
                let explanationHtml = "";
                set.questions.forEach(sq => {
                    if (sq.explanation) {
                        explanationHtml += `
                            <div class="explanation-box" style="margin-bottom: 16px; padding: 14px 18px; border: 1px solid var(--border); border-left: 4px solid var(--color-blue); background: rgba(59, 130, 246, 0.015);">
                                <h5 style="color: var(--color-blue); margin: 0 0 8px 0; font-size: 0.95rem; font-weight: 800; text-transform: uppercase;">
                                    Giải thích QUESTION ${sq.id}:
                                </h5>
                                <div style="font-size: 0.9rem; line-height: 1.5; color: var(--text-main);">
                                    ${sq.explanation}
                                </div>
                            </div>
                        `;
                    }
                });
                
                const transcriptHtml = renderTranscriptHtml(set.transcript, set.vietnamese_transcript);
                const scriptCard = document.createElement("div");
                scriptCard.innerHTML = renderScriptCardHtml(`exset-${set.set_index}`, transcriptHtml, explanationHtml);
                const innerScriptCard = scriptCard.firstElementChild;
                innerScriptCard.classList.add("hidden");
                
                setWrapper.appendChild(innerScriptCard);
                hookScriptCardToggler(`exset-${set.set_index}`);
                
                submitBtn.addEventListener("click", () => {
                    let setCorrectCount = 0;
                    set.questions.forEach(q => {
                        const key = userSelections[q.slide_index];
                        const qOptions = qListDiv.querySelectorAll(`.choice-option[data-q-slide="${q.slide_index}"]`);
                        qOptions.forEach(o => {
                            const oKey = o.getAttribute("data-key");
                            o.classList.remove("selected");
                            o.classList.add("checked-done");
                            if (oKey === q.answer) {
                                o.classList.add("correct");
                            } else if (oKey === key) {
                                o.classList.add("incorrect");
                            }
                            const t = o.querySelector(".c-trans");
                            if (t) t.style.display = "block";
                        });
                        if (key === q.answer) {
                            spawnConfetti(25);
                            setCorrectCount++;
                        }
                    });
                    if (setCorrectCount >= 2) {
                        SoundEffects.playCorrect();
                    } else {
                        SoundEffects.playWrong();
                    }
                    innerScriptCard.classList.remove("hidden");
                    submitBtn.style.display = "none";
                });
                
                examplesContentAreaP4.appendChild(setWrapper);
            });
        } else {
            // Render single examples for subsections
            section.examples.forEach((ex, exIdx) => {
                const wrapper = document.createElement("div");
                wrapper.className = "question-wrapper-group";
                wrapper.style.marginBottom = "24px";
                
                const audioDiv = document.createElement("div");
                wrapper.appendChild(audioDiv);
                createAudioPlayer(ex.audio, audioDiv);
                
                const qCard = document.createElement("div");
                qCard.className = "question-block";
                qCard.style.padding = "24px";
                
                const choicesHtml = renderChoicesHtml(ex, false);
                const questionTextHtml = renderQuestionTextHtml(ex, `ex-single-${ex.slide_index}`, `<strong>EXAMPLE ${exIdx + 1}:</strong> `);
                
                let explanationHtml = "";
                if (ex.explanation) {
                    explanationHtml = `
                        <div class="explanation-box" style="margin-bottom: 16px; padding: 14px 18px; border: 1px solid var(--border); border-left: 4px solid var(--color-blue); background: rgba(59, 130, 246, 0.015);">
                            <h5 style="color: var(--color-blue); margin: 0 0 8px 0; font-size: 0.95rem; font-weight: 800; text-transform: uppercase;">
                                GIẢI THÍCH ĐÁP ÁN:
                            </h5>
                            <div style="font-size: 0.9rem; line-height: 1.5; color: var(--text-main);">
                                ${ex.explanation}
                            </div>
                        </div>
                    `;
                }
                
                const transcriptHtml = renderTranscriptHtml(ex.transcript, ex.vietnamese_transcript);
                
                qCard.innerHTML = `
                    ${questionTextHtml}
                    <div class="choices-stack" style="margin-top: 16px;">
                        ${choicesHtml}
                    </div>
                    <div style="margin-top: 16px; text-align: right;">
                        <button class="btn btn-primary" id="btn-check-ex-${ex.slide_index}" style="padding: 10px 20px; font-weight: 700; border-radius: 0px !important;" disabled>KIỂM TRA</button>
                    </div>
                    ${renderScriptCardHtml(`ex-${ex.slide_index}`, transcriptHtml, explanationHtml)}
                `;
                
                wrapper.appendChild(qCard);
                examplesContentAreaP4.appendChild(wrapper);
                hookScriptCardToggler(`ex-${ex.slide_index}`);
                
                const checkBtn = qCard.querySelector(`#btn-check-ex-${ex.slide_index}`);
                const options = qCard.querySelectorAll(".choice-option");
                let selectedKey = null;

                options.forEach(opt => {
                    opt.addEventListener("click", () => {
                        if (opt.classList.contains("checked-done")) {
                            const t = opt.querySelector(".c-trans");
                            if (t) t.style.display = t.style.display === "block" ? "none" : "block";
                            return;
                        }
                        
                        // Toggle option translation inline on click
                        const t = opt.querySelector(".c-trans");
                        if (t) t.style.display = t.style.display === "block" ? "none" : "block";
                        
                        selectedKey = opt.getAttribute("data-key");
                        options.forEach(o => o.classList.remove("selected"));
                        opt.classList.add("selected");
                        checkBtn.disabled = false;
                    });
                });

                checkBtn.addEventListener("click", () => {
                    options.forEach(o => {
                        const oKey = o.getAttribute("data-key");
                        o.classList.remove("selected");
                        o.classList.add("checked-done");
                        if (oKey === ex.answer) {
                            o.classList.add("correct");
                        } else if (oKey === selectedKey) {
                            o.classList.add("incorrect");
                        }
                    });
                    if (selectedKey === ex.answer) {
                        spawnConfetti(35);
                        SoundEffects.playCorrect();
                    } else {
                        SoundEffects.playWrong();
                    }
                    const scriptCardElement = qCard.querySelector(`#reveal-card-ex-${ex.slide_index}`);
                    if (scriptCardElement) scriptCardElement.classList.remove("hidden");
                    checkBtn.style.display = "none";
                });
            });
        }
    }
    
    // D. PRACTICE EXERCISES
    function renderPracticeP4(section) {
        practiceContentAreaP4.innerHTML = "";
        
        if (section.type === "subsection" || section.type === "overview" || section.type === "tips") {
            renderPracticeQuestionsP4(section.practice, section);
        } else if (section.type === "topic" || section.type === "test") {
            renderPracticeSetsP4(section.practice_sets, section);
        }
    }
    
    function renderPracticeQuestionsP4(questions, section) {
        if (!questions || questions.length === 0) {
            practiceContentAreaP4.innerHTML = "<p style='color: var(--text-muted); font-weight: 700;'>Bài tập đang được cập nhật.</p>";
            return;
        }

        // Initialize quiz state if needed
        if (!state.quiz.questions || state.quiz.sectionId !== section.id) {
            state.quiz = {
                sectionId: section.id,
                questions: questions,
                currentIdx: 0,
                score: 0,
                reviewMode: false,
                answers: {}
            };
        }

        if (state.quiz.reviewMode) {
            renderPracticeQuestionsReviewP4(questions, section);
            return;
        }

        const currentIdx = state.quiz.currentIdx;
        
        if (currentIdx >= questions.length) {
            renderPracticeQuestionsSummaryP4(questions, section);
            return;
        }

        const q = questions[currentIdx];
        practiceContentAreaP4.innerHTML = "";

        // Progress Header
        const progressHeader = document.createElement("div");
        progressHeader.className = "quiz-progress-header";
        progressHeader.style.display = "flex";
        progressHeader.style.justifyContent = "space-between";
        progressHeader.style.alignItems = "center";
        progressHeader.style.marginBottom = "20px";
        progressHeader.style.padding = "14px 20px";
        progressHeader.style.background = "rgba(255, 255, 255, 0.015)";
        progressHeader.style.border = "1px solid var(--border)";
        
        const progressText = document.createElement("span");
        progressText.style.fontWeight = "700";
        progressText.style.fontSize = "0.9rem";
        progressText.style.color = "var(--text-main)";
        progressText.textContent = `CÂU HỎI ${currentIdx + 1} / ${questions.length}`;
        
        const scoreText = document.createElement("span");
        scoreText.className = "score-text-display";
        scoreText.style.fontWeight = "800";
        scoreText.style.fontSize = "0.95rem";
        scoreText.textContent = `ĐÚNG: ${state.quiz.score} / ${questions.length}`;
        
        progressHeader.appendChild(progressText);
        progressHeader.appendChild(scoreText);
        practiceContentAreaP4.appendChild(progressHeader);

        // Active Question Card
        const wrapper = document.createElement("div");
        wrapper.className = "question-wrapper-group";
        wrapper.style.marginBottom = "24px";
        
        const audioDiv = document.createElement("div");
        wrapper.appendChild(audioDiv);
        createAudioPlayer(q.audio, audioDiv);
        
        const qCard = document.createElement("div");
        qCard.className = "question-block";
        qCard.style.padding = "24px";
        
        const choicesHtml = renderChoicesHtml(q, false);
        const questionTextHtml = renderQuestionTextHtml(q, `pr-${q.slide_index}`, `<strong>QUESTION:</strong> `);
        
        let explanationHtml = "";
        if (q.explanation) {
            explanationHtml = `
                <div class="explanation-box" style="margin-bottom: 16px; padding: 14px 18px; border: 1px solid var(--border); border-left: 4px solid var(--color-blue); background: rgba(59, 130, 246, 0.015);">
                    <h5 style="color: var(--color-blue); margin: 0 0 8px 0; font-size: 0.95rem; font-weight: 800; text-transform: uppercase;">
                        GIẢI THÍCH ĐÁP ÁN:
                    </h5>
                    <div style="font-size: 0.9rem; line-height: 1.5; color: var(--text-main);">
                        ${q.explanation}
                    </div>
                </div>
            `;
        }
        const transcriptHtml = renderTranscriptHtml(q.transcript, q.vietnamese_transcript);
        
        qCard.innerHTML = `
            ${questionTextHtml}
            <div class="choices-stack" style="margin-top: 16px;">
                ${choicesHtml}
            </div>
            ${renderScriptCardHtml(`pr-${q.slide_index}`, transcriptHtml, explanationHtml)}
            <div class="quiz-action-row" style="margin-top: 24px; display: flex; justify-content: space-between; align-items: center;">
                <button class="btn btn-primary" id="quiz-check-btn" style="padding: 12px 24px; font-weight: 700; border-radius: 0px !important;" disabled>
                    KIỂM TRA
                </button>
                <div style="flex:1;"></div>
                <button class="btn btn-primary" id="quiz-next-btn" style="display: none; padding: 12px 24px; font-weight: 700; border-radius: 0px !important; align-items: center; gap: 6px;">
                    CÂU TIẾP THEO <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle;"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </button>
            </div>
        `;
        
        wrapper.appendChild(qCard);
        practiceContentAreaP4.appendChild(wrapper);
        hookScriptCardToggler(`pr-${q.slide_index}`);
        
        const checkBtn = qCard.querySelector("#quiz-check-btn");
        const nextBtn = qCard.querySelector("#quiz-next-btn");
        const options = qCard.querySelectorAll(".choice-option");
        let selectedKey = null;
        
        options.forEach(opt => {
            opt.addEventListener("click", () => {
                if (opt.classList.contains("checked-done")) {
                    const t = opt.querySelector(".c-trans");
                    if (t) t.style.display = t.style.display === "block" ? "none" : "block";
                    return;
                }
                
                // Toggle option translation inline on click
                const t = opt.querySelector(".c-trans");
                if (t) t.style.display = t.style.display === "block" ? "none" : "block";
                
                selectedKey = opt.getAttribute("data-key");
                options.forEach(o => o.classList.remove("selected"));
                opt.classList.add("selected");
                checkBtn.disabled = false;
            });
        });
        
        checkBtn.addEventListener("click", () => {
            state.quiz.answers[q.slide_index] = selectedKey;
            
            options.forEach(o => {
                const oKey = o.getAttribute("data-key");
                o.classList.remove("selected");
                o.classList.add("checked-done");
                if (oKey === q.answer) {
                    o.classList.add("correct");
                } else if (oKey === selectedKey) {
                    o.classList.add("incorrect");
                }
            });
            
            markQuestionAnswered(q.slide_index);
            
            const isCorrect = selectedKey === q.answer;
            if (isCorrect) {
                state.quiz.score++;
                scoreText.textContent = `ĐÚNG: ${state.quiz.score} / ${questions.length}`;
                spawnConfetti(35);
                SoundEffects.playCorrect();
            } else {
                SoundEffects.playWrong();
            }
            
            // Submit to Google Forms background
            const studentName = localStorage.getItem("studentName") || "Ẩn danh";
            submitToGoogleForm(studentName, `${section.title} - Câu ${currentIdx + 1}`, "Luyện tập (Câu)", isCorrect ? 1 : 0, 1);
            
            const scriptCardElement = qCard.querySelector(`#reveal-card-pr-${q.slide_index}`);
            if (scriptCardElement) scriptCardElement.classList.remove("hidden");
            
            checkBtn.style.display = "none";
            nextBtn.style.display = "flex";
        });
        
        nextBtn.addEventListener("click", () => {
            state.quiz.currentIdx++;
            renderPracticeQuestions(questions, section);
        });
    }

    function renderPracticeQuestionsSummary(questions, section) {
        practiceContentAreaP4.innerHTML = "";
        
        const score = state.quiz.score;
        const total = questions.length;
        
        let msg = "";
        if (score === total) {
            msg = "QUÁ XUẤT SẮC! Bạn đã trả lời đúng toàn bộ câu hỏi. Hãy tiếp tục phát huy phong độ này nhé!";
            let count = 0;
            const interval = setInterval(() => {
                spawnConfetti(45, true); // Gold only
                count++;
                if (count > 5) clearInterval(interval);
            }, 400);
        } else if (score >= total * 0.7) {
            msg = "RẤT TỐT! Kỹ năng nghe của bạn khá vững vàng. Hãy xem lại các câu sai để rút kinh nghiệm nhé.";
            spawnConfetti(50);
        } else {
            msg = "CỐ GẮNG LÊN! Bạn cần luyện tập thêm. Hãy dành thời gian xem lại transcript và từ vựng của dạng bài này.";
        }
        
        const summaryCard = document.createElement("div");
        summaryCard.className = "quiz-summary-card";
        summaryCard.style.textAlign = "center";
        summaryCard.style.padding = "48px 40px";
        summaryCard.style.border = "1px solid var(--border)";
        summaryCard.style.background = "rgba(255, 255, 255, 0.015)";
        
        summaryCard.innerHTML = `
            <div style="font-size: 3.5rem; color: var(--color-gold); margin-bottom: 20px;">🏆</div>
            <h3 style="font-size: 1.6rem; margin-bottom: 12px; font-weight: 800; text-transform: uppercase;">KẾT QUẢ BÀI TẬP</h3>
            <div style="font-size: 2.8rem; font-weight: 800; color: var(--color-blue); margin-bottom: 16px;">
                ${score} / ${total}
            </div>
            <p style="color: var(--text-muted); font-size: 1.05rem; margin-bottom: 36px; line-height: 1.7; max-width: 500px; margin-left: auto; margin-right: auto;">${msg}</p>
            <div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap;">
                <button class="btn btn-primary" id="btn-quiz-retry" style="padding: 12px 24px; font-weight: 700; border-radius: 0px !important;">LÀM LẠI BÀI TẬP</button>
                <button class="btn btn-secondary" id="btn-quiz-review" style="padding: 12px 24px; font-weight: 700; border-radius: 0px !important;">XEM LẠI ĐÁP ÁN</button>
            </div>
        `;
        
        practiceContentAreaP4.appendChild(summaryCard);
        
        document.getElementById("btn-quiz-retry").addEventListener("click", () => {
            state.quiz = {
                sectionId: section.id,
                questions: questions,
                currentIdx: 0,
                score: 0,
                reviewMode: false,
                answers: {}
            };
            // Clear progress
            questions.forEach(q => {
                delete state.answeredQuestions[q.slide_index];
            });
            updateRouteProgress();
            try {
                localStorage.setItem("toeic_answered_questions", JSON.stringify(state.answeredQuestions));
            } catch (e) {}
            
            renderPracticeQuestions(questions, section);
        });
        
        document.getElementById("btn-quiz-review").addEventListener("click", () => {
            state.quiz.reviewMode = true;
            renderPracticeQuestions(questions, section);
        });
    }

    function renderPracticeQuestionsReview(questions, section) {
        practiceContentAreaP4.innerHTML = "";
        
        // Review Header
        const reviewHeader = document.createElement("div");
        reviewHeader.className = "quiz-progress-header";
        reviewHeader.style.display = "flex";
        reviewHeader.style.justifyContent = "space-between";
        reviewHeader.style.alignItems = "center";
        reviewHeader.style.marginBottom = "24px";
        reviewHeader.style.padding = "14px 20px";
        reviewHeader.style.background = "rgba(255, 255, 255, 0.015)";
        reviewHeader.style.border = "1px solid var(--border)";
        
        const reviewTitle = document.createElement("span");
        reviewTitle.style.fontWeight = "700";
        reviewTitle.style.fontSize = "0.9rem";
        reviewTitle.textContent = "XEM LẠI ĐÁP ÁN & TRANSCRIPT";
        
        const backBtn = document.createElement("button");
        backBtn.className = "mini-btn";
        backBtn.style.padding = "6px 12px";
        backBtn.textContent = "QUAY LẠI TỔNG KẾT";
        backBtn.style.borderRadius = "0px !important";
        backBtn.addEventListener("click", () => {
            state.quiz.currentIdx = questions.length; // triggers summary view
            renderPracticeQuestions(questions, section);
        });
        
        reviewHeader.appendChild(reviewTitle);
        reviewHeader.appendChild(backBtn);
        practiceContentAreaP4.appendChild(reviewHeader);

        // List all questions
        questions.forEach((q, idx) => {
            const wrapper = document.createElement("div");
            wrapper.className = "question-wrapper-group";
            wrapper.style.marginBottom = "28px";
            
            const audioDiv = document.createElement("div");
            wrapper.appendChild(audioDiv);
            createAudioPlayer(q.audio, audioDiv);
            
            const qCard = document.createElement("div");
            qCard.className = "question-block";
            qCard.style.padding = "24px";
            
            const userAnswer = state.quiz.answers[q.slide_index];
            const choicesHtml = renderChoicesHtml(q, true, userAnswer);
            
            let badgeText = userAnswer === q.answer ? 
                `<span style="color: var(--success); margin-left: 10px; font-size: 0.9rem; font-weight: 700;">✔️ ĐÚNG</span>` : 
                `<span style="color: var(--danger); margin-left: 10px; font-size: 0.85rem; font-weight: 700;">❌ SAI (Chọn ${userAnswer || "Trống"})</span>`;
            
            const questionTextHtml = renderQuestionTextHtml(q, `rev-q-${q.slide_index}`, `<strong>QUESTION ${idx + 1}:</strong> `);
            
            let explanationHtml = "";
            if (q.explanation) {
                explanationHtml = `
                    <div class="explanation-box" style="margin-bottom: 16px; padding: 14px 18px; border: 1px solid var(--border); border-left: 4px solid var(--color-blue); background: rgba(59, 130, 246, 0.015);">
                        <h5 style="color: var(--color-blue); margin: 0 0 8px 0; font-size: 0.95rem; font-weight: 800; text-transform: uppercase;">
                            GIẢI THÍCH ĐÁP ÁN:
                        </h5>
                        <div style="font-size: 0.9rem; line-height: 1.5; color: var(--text-main);">
                            ${q.explanation}
                        </div>
                    </div>
                `;
            }
            const transcriptHtml = renderTranscriptHtml(q.transcript, q.vietnamese_transcript);
            
            qCard.innerHTML = `
                <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom: 10px; width:100%;">
                    <div style="flex:1;">${questionTextHtml}</div>
                    <div>${badgeText}</div>
                </div>
                <div class="choices-stack" style="margin-top: 16px;">
                    ${choicesHtml}
                </div>
                ${renderScriptCardHtml(`rev-${q.slide_index}`, transcriptHtml, explanationHtml)}
            `;
            
            wrapper.appendChild(qCard);
            practiceContentAreaP4.appendChild(wrapper);
            
            const revCard = qCard.querySelector(`.reveal-script-card`);
            if (revCard) revCard.classList.remove("hidden");
            hookScriptCardToggler(`rev-${q.slide_index}`);
        });
    }

    // E. PRACTICE SETS (FOR TOPICS)
    function renderPracticeSetsP4(sets, section) {
        if (!sets || sets.length === 0) {
            practiceContentAreaP4.innerHTML = "<p style='color: var(--text-muted); font-weight: 700;'>Bài tập đang được cập nhật.</p>";
            return;
        }

        // Initialize set quiz state if needed
        if (!state.setQuiz.sets || state.setQuiz.sectionId !== section.id) {
            state.setQuiz = {
                sectionId: section.id,
                sets: sets,
                currentIdx: 0,
                completedSets: {}, // set_index -> score
                reviewMode: false,
                answers: {}
            };
        }

        if (state.setQuiz.reviewMode) {
            renderPracticeSetsReviewP4(sets, section);
            return;
        }

        const currentIdx = state.setQuiz.currentIdx;
        
        if (currentIdx >= sets.length) {
            renderPracticeSetsSummaryP4(sets, section);
            return;
        }

        const set = sets[currentIdx];
        practiceContentAreaP4.innerHTML = "";
        practiceContentAreaP4.style.maxWidth = "1000px";
        practiceContentAreaP4.style.margin = "0 auto";

        // Progress Header
        const progressHeader = document.createElement("div");
        progressHeader.className = "quiz-progress-header";
        progressHeader.style.display = "flex";
        progressHeader.style.justifyContent = "space-between";
        progressHeader.style.alignItems = "center";
        progressHeader.style.marginBottom = "20px";
        progressHeader.style.padding = "14px 20px";
        progressHeader.style.background = "rgba(255, 255, 255, 0.015)";
        progressHeader.style.border = "1px solid var(--border)";
        
        const progressText = document.createElement("span");
        progressText.style.fontWeight = "700";
        progressText.style.fontSize = "0.9rem";
        progressText.textContent = `ĐOẠN HỘI THOẠI ${currentIdx + 1} / ${sets.length}`;
        
        const completedCount = Object.keys(state.setQuiz.completedSets).length;
        const progressScore = document.createElement("span");
        progressScore.style.fontWeight = "800";
        progressScore.style.fontSize = "0.95rem";
        progressScore.style.color = "var(--color-blue)";
        progressScore.textContent = `HOÀN THÀNH: ${completedCount} / ${sets.length}`;
        
        progressHeader.appendChild(progressText);
        progressHeader.appendChild(progressScore);
        practiceContentAreaP4.appendChild(progressHeader);

        // Navigator Row
        const navigatorRow = document.createElement("div");
        navigatorRow.className = "quiz-navigator-row";
        navigatorRow.style.display = "flex";
        navigatorRow.style.flexWrap = "wrap";
        navigatorRow.style.gap = "8px";
        navigatorRow.style.marginBottom = "20px";
        navigatorRow.style.justifyContent = "center";
        
        sets.forEach((s, idx) => {
            const navBtn = document.createElement("button");
            navBtn.style.padding = "8px 14px";
            navBtn.style.fontSize = "0.85rem";
            navBtn.style.fontWeight = "700";
            navBtn.style.border = "1px solid var(--border)";
            navBtn.style.cursor = "pointer";
            navBtn.style.minWidth = "36px";
            navBtn.style.borderRadius = "0px";
            navBtn.style.transition = "all 0.2s ease";
            
            navBtn.textContent = idx + 1;
            
            const isCompleted = state.setQuiz.completedSets[s.set_index] !== undefined;
            
            if (idx === currentIdx) {
                navBtn.style.background = "var(--color-blue)";
                navBtn.style.color = "white";
                navBtn.style.borderColor = "var(--color-blue)";
            } else if (isCompleted) {
                navBtn.style.background = "rgba(16, 185, 129, 0.15)";
                navBtn.style.color = "#10b981";
                navBtn.style.borderColor = "#10b981";
            } else {
                navBtn.style.background = "transparent";
                navBtn.style.color = "var(--text-main)";
            }
            
            navBtn.addEventListener("click", () => {
                state.setQuiz.currentIdx = idx;
                renderPracticeSetsP4(sets, section);
            });
            
            navigatorRow.appendChild(navBtn);
        });
        
        practiceContentAreaP4.appendChild(navigatorRow);

        // Set Card Wrapper
        const setWrapper = document.createElement("div");
        setWrapper.className = "practice-set-card";
        setWrapper.style.padding = "24px";
        setWrapper.style.border = "1px solid var(--border)";
        setWrapper.style.background = "rgba(255, 255, 255, 0.01)";
        
        const setHeader = document.createElement("h3");
        setHeader.style.fontSize = "1.1rem";
        setHeader.style.marginBottom = "16px";
        setHeader.style.fontWeight = "800";
        setHeader.textContent = `LUYỆN TẬP ĐOẠN HỘI THOẠI ${set.set_index}`;
        setWrapper.appendChild(setHeader);
        
        const audioDiv = document.createElement("div");
        setWrapper.appendChild(audioDiv);
        createAudioPlayer(set.audio, audioDiv);
        
        if (set.image) {
            const imgDiv = document.createElement("div");
            imgDiv.style.textAlign = "center";
            imgDiv.style.marginTop = "20px";
            imgDiv.style.marginBottom = "20px";
            imgDiv.innerHTML = `<img src="data/graphics/part04/${set.image}" alt="Graphic for Set ${set.set_index}" style="max-width: 100%; max-height: 400px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">`;
            setWrapper.appendChild(imgDiv);
        }
        
        const qListDiv = document.createElement("div");
        setWrapper.appendChild(qListDiv);
        
        const userSelections = {};
        const setAlreadySubmitted = state.setQuiz.completedSets[set.set_index] !== undefined;

        set.questions.forEach(q => {
            const qCard = document.createElement("div");
            qCard.className = "question-block";
            qCard.style.padding = "20px";
            qCard.style.marginTop = "16px";
            
            const savedAns = state.setQuiz.answers[q.slide_index];
            const choicesHtml = renderChoicesHtml(q, setAlreadySubmitted, savedAns);
            const questionTextHtml = renderQuestionTextHtml(q, `set-q-${q.slide_index}`, `<strong>QUESTION ${q.id}:</strong> `);
            
            qCard.innerHTML = `
                ${questionTextHtml}
                <div class="choices-stack" style="margin-top: 12px;">
                    ${choicesHtml}
                </div>
            `;
            
            qListDiv.appendChild(qCard);
            
            if (!setAlreadySubmitted) {
                const options = qCard.querySelectorAll(".choice-option");
                options.forEach(opt => {
                    opt.addEventListener("click", () => {
                        // Toggle option translation inline on click
                        const t = opt.querySelector(".c-trans");
                        if (t) t.style.display = t.style.display === "block" ? "none" : "block";
                        
                        const key = opt.getAttribute("data-key");
                        userSelections[q.slide_index] = key;
                        state.setQuiz.answers[q.slide_index] = key;
                        
                        options.forEach(o => o.classList.remove("selected"));
                        opt.classList.add("selected");
                        
                        // Enable submit button only if all questions answered
                        let allSelected = true;
                        set.questions.forEach(qi => {
                            if (!userSelections[qi.slide_index]) {
                                allSelected = false;
                            }
                        });
                        
                        if (allSelected) {
                            submitBtn.disabled = false;
                        }
                    });
                });
            }
        });
        
        const submitRow = document.createElement("div");
        submitRow.className = "submit-row";
        submitRow.style.marginTop = "24px";
        submitRow.style.display = "flex";
        submitRow.style.justifyContent = "space-between";
        submitRow.style.alignItems = "center";
        submitRow.style.gap = "12px";
        
        // Left Column: Quay lại button
        const leftCol = document.createElement("div");
        leftCol.style.flex = "1";
        leftCol.style.textAlign = "left";
        if (currentIdx > 0) {
            const prevBtn = document.createElement("button");
            prevBtn.className = "action-btn btn-secondary";
            prevBtn.style.padding = "12px 20px";
            prevBtn.style.background = "transparent";
            prevBtn.style.border = "1px solid var(--border)";
            prevBtn.style.color = "var(--text-main)";
            prevBtn.style.cursor = "pointer";
            prevBtn.style.borderRadius = "0px";
            prevBtn.innerHTML = `&larr; QUAY LẠI`;
            prevBtn.addEventListener("click", () => {
                state.setQuiz.currentIdx--;
                renderPracticeSetsP4(sets, section);
            });
            leftCol.appendChild(prevBtn);
        }
        submitRow.appendChild(leftCol);
        
        // Center Column: Submit button or result score
        const centerCol = document.createElement("div");
        centerCol.style.flex = "2";
        centerCol.style.display = "flex";
        centerCol.style.justifyContent = "center";
        centerCol.style.alignItems = "center";
        centerCol.style.gap = "16px";
        
        const scoreSpan = document.createElement("span");
        scoreSpan.className = "score-display";
        scoreSpan.style.fontWeight = "800";
        scoreSpan.style.fontSize = "1.05rem";
        scoreSpan.style.color = "var(--color-blue)";
        
        const submitBtn = document.createElement("button");
        submitBtn.className = "action-btn btn-primary";
        submitBtn.style.padding = "12px 24px";
        submitBtn.textContent = "NỘP BÀI TRẢ LỜI";
        submitBtn.disabled = true;
        submitBtn.style.borderRadius = "0px !important";
        
        if (setAlreadySubmitted) {
            const score = state.setQuiz.completedSets[set.set_index];
            scoreSpan.textContent = `Kết quả: ${score} / ${set.questions.length} câu đúng`;
        }
        
        centerCol.appendChild(scoreSpan);
        if (!setAlreadySubmitted) {
            centerCol.appendChild(submitBtn);
        }
        submitRow.appendChild(centerCol);
        
        // Right Column: Next / Skip buttons
        const rightCol = document.createElement("div");
        rightCol.style.flex = "1";
        rightCol.style.textAlign = "right";
        
        const nextBtn = document.createElement("button");
        nextBtn.className = "action-btn btn-primary";
        nextBtn.style.padding = "12px 24px";
        nextBtn.innerHTML = `ĐOẠN TIẾP THEO &rarr;`;
        nextBtn.style.borderRadius = "0px !important";
        nextBtn.style.display = "none";
        
        const skipBtn = document.createElement("button");
        skipBtn.className = "action-btn btn-secondary";
        skipBtn.style.padding = "12px 20px";
        skipBtn.style.background = "transparent";
        skipBtn.style.border = "1px solid var(--border)";
        skipBtn.style.color = "var(--text-muted)";
        skipBtn.style.cursor = "pointer";
        skipBtn.style.borderRadius = "0px";
        skipBtn.innerHTML = `BỎ QUA &rarr;`;
        skipBtn.style.display = "none";
        
        skipBtn.addEventListener("click", () => {
            state.setQuiz.currentIdx++;
            renderPracticeSetsP4(sets, section);
        });
        
        if (currentIdx < sets.length - 1) {
            rightCol.appendChild(nextBtn);
            rightCol.appendChild(skipBtn);
            
            if (setAlreadySubmitted) {
                nextBtn.style.display = "flex";
            } else {
                skipBtn.style.display = "flex";
            }
        }
        
        submitRow.appendChild(rightCol);
        setWrapper.appendChild(submitRow);
        
        // Transcript & Explanations Card
        let explanationHtml = "";
        set.questions.forEach(sq => {
            if (sq.explanation) {
                explanationHtml += `
                    <div class="explanation-box" style="margin-bottom: 16px; padding: 14px 18px; border: 1px solid var(--border); border-left: 4px solid var(--color-blue); background: rgba(59, 130, 246, 0.015);">
                        <h5 style="color: var(--color-blue); margin: 0 0 8px 0; font-size: 0.95rem; font-weight: 800; text-transform: uppercase;">
                            Giải thích QUESTION ${sq.id}:
                        </h5>
                        <div style="font-size: 0.9rem; line-height: 1.5; color: var(--text-main);">
                            ${sq.explanation}
                        </div>
                    </div>
                `;
            }
        });
        
        const transcriptHtml = renderTranscriptHtml(set.transcript, set.vietnamese_transcript);
        const scriptCard = document.createElement("div");
        scriptCard.innerHTML = renderScriptCardHtml(`set-${set.set_index}`, transcriptHtml, explanationHtml);
        const innerScriptCard = scriptCard.firstElementChild;
        if (!setAlreadySubmitted) {
            innerScriptCard.classList.add("hidden");
        }
        
        setWrapper.appendChild(innerScriptCard);
        hookScriptCardToggler(`set-${set.set_index}`);
        
        const submitHandler = () => {
            const numQs = set.questions.length;
            let correctCount = 0;
            
            set.questions.forEach(q => {
                const userVal = userSelections[q.slide_index];
                const correctVal = q.answer;
                
                const qOptions = qListDiv.querySelectorAll(`.choice-option[data-q-slide="${q.slide_index}"]`);
                qOptions.forEach(o => {
                    const oKey = o.getAttribute("data-key");
                    o.classList.remove("correct", "selected");
                    o.classList.add("checked-done");
                    
                    if (oKey === correctVal) {
                        o.classList.add("correct");
                    } else if (oKey === userVal) {
                        o.classList.add("incorrect");
                    }
                    const t = o.querySelector(".c-trans");
                    if (t) t.style.display = "block";
                });
                
                if (userVal === correctVal) {
                    correctCount++;
                }
                
                markQuestionAnswered(q.slide_index);
            });
            
            state.setQuiz.completedSets[set.set_index] = correctCount;
            
            scoreSpan.textContent = `Kết quả: ${correctCount} / ${numQs} câu đúng`;
            submitBtn.style.display = "none";
            if (currentIdx < sets.length - 1) {
                skipBtn.style.display = "none";
                nextBtn.style.display = "flex";
            }
            innerScriptCard.classList.remove("hidden");
            
            // Show result modal
            modalScore.textContent = correctCount;
            modalTotal.textContent = `/${numQs}`;
            
            let msg = "";
            if (correctCount === numQs) {
                msg = "Tuyệt vời! Bạn đã xuất sắc trả lời đúng tất cả các câu hỏi. Hãy tiếp tục phát huy nhé!";
                SoundEffects.playCorrect();
                let count = 0;
                const interval = setInterval(() => {
                    spawnConfetti(40, true);
                    count++;
                    if (count > 5) clearInterval(interval);
                }, 450);
            } else if (correctCount >= 2) {
                msg = "Khá tốt! Bạn đã trả lời đúng phần lớn câu hỏi. Hãy xem lại transcript để củng cố câu sai nhé.";
                SoundEffects.playCorrect();
                spawnConfetti(50);
            } else {
                msg = "Cố gắng lên! Bạn cần luyện tập thêm. Hãy xem lại transcript và từ vựng để cải thiện kỹ năng nghe.";
                SoundEffects.playWrong();
            }
            modalMessage.textContent = msg;
            
            // Submit to Google Forms background
            const studentName = localStorage.getItem("studentName") || "Ẩn danh";
            submitToGoogleForm(studentName, section.title, `Luyện tập (Đoạn ${set.set_index})`, correctCount, numQs);
            
            modalReviewBtn.onclick = () => {
                resultModal.classList.add("hidden");
            };
            
            modalRetryBtn.onclick = () => {
                resultModal.classList.add("hidden");
                scoreSpan.textContent = "";
                submitBtn.style.display = "flex";
                submitBtn.disabled = true;
                nextBtn.style.display = "none";
                innerScriptCard.classList.add("hidden");
                
                delete state.setQuiz.completedSets[set.set_index];
                
                set.questions.forEach(q => {
                    delete userSelections[q.slide_index];
                    delete state.setQuiz.answers[q.slide_index];
                    delete state.answeredQuestions[q.slide_index];
                    
                    const qOptions = qListDiv.querySelectorAll(`.choice-option[data-q-slide="${q.slide_index}"]`);
                    qOptions.forEach(o => {
                        o.classList.remove("checked-done", "correct", "incorrect");
                        o.disabled = false;
                    });
                });
                
                updateRouteProgress();
            };
            
            resultModal.classList.remove("hidden");
        };
        
        submitBtn.addEventListener("click", submitHandler);
        
        nextBtn.addEventListener("click", () => {
            state.setQuiz.currentIdx++;
            renderPracticeSetsP4(sets, section);
        });
        
        practiceContentAreaP4.appendChild(setWrapper);
    }

    function renderPracticeSetsSummaryP4(sets, section) {
        practiceContentAreaP4.innerHTML = "";
        
        let totalScore = 0;
        let totalQs = 0;
        
        sets.forEach(set => {
            totalScore += state.setQuiz.completedSets[set.set_index] || 0;
            totalQs += set.questions.length;
        });
        
        let msg = "";
        if (totalScore === totalQs) {
            msg = "THẬT SỰ QUÁ ĐỈNH! Bạn đã hoàn thành xuất sắc toàn bộ các đoạn hội thoại với số điểm tối đa.";
            let count = 0;
            const interval = setInterval(() => {
                spawnConfetti(45, true);
                count++;
                if (count > 6) clearInterval(interval);
            }, 400);
        } else if (totalScore >= totalQs * 0.7) {
            msg = "CỰC KỲ TỐT! Kỹ năng nghe hiểu đoạn hội thoại dài của bạn rất ấn tượng. Hãy xem lại các lỗi nhỏ nhé.";
            spawnConfetti(55);
        } else {
            msg = "CỐ GẮNG LÊN! Luyện nghe đoạn hội thoại dài cần kiên trì. Hãy dành thời gian xem kỹ transcript và nghe lại nhiều lần.";
        }
        
        const summaryCard = document.createElement("div");
        summaryCard.className = "quiz-summary-card";
        summaryCard.style.textAlign = "center";
        summaryCard.style.padding = "48px 40px";
        summaryCard.style.border = "1px solid var(--border)";
        summaryCard.style.background = "rgba(255, 255, 255, 0.015)";
        
        summaryCard.innerHTML = `
            <div style="font-size: 3.5rem; color: var(--color-gold); margin-bottom: 20px;">🏆</div>
            <h3 style="font-size: 1.6rem; margin-bottom: 12px; font-weight: 800; text-transform: uppercase;">KẾT QUẢ CHỦ ĐỀ LUYỆN TẬP</h3>
            <div style="font-size: 2.8rem; font-weight: 800; color: var(--color-blue); margin-bottom: 16px;">
                ${totalScore} / ${totalQs}
            </div>
            <p style="color: var(--text-muted); font-size: 1.05rem; margin-bottom: 36px; line-height: 1.7; max-width: 500px; margin-left: auto; margin-right: auto;">${msg}</p>
            <div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap;">
                <button class="btn btn-primary" id="btn-set-retry" style="padding: 12px 24px; font-weight: 700; border-radius: 0px !important;">LÀM LẠI TOÀN BỘ</button>
                <button class="btn btn-secondary" id="btn-set-review" style="padding: 12px 24px; font-weight: 700; border-radius: 0px !important;">XEM LẠI CÁC ĐÁP ÁN</button>
            </div>
        `;
        
        practiceContentAreaP4.appendChild(summaryCard);
        
        document.getElementById("btn-set-retry").addEventListener("click", () => {
            state.setQuiz = {
                sectionId: section.id,
                sets: sets,
                currentIdx: 0,
                completedSets: {},
                reviewMode: false,
                answers: {}
            };
            
            sets.forEach(set => {
                set.questions.forEach(q => {
                    delete state.answeredQuestions[q.slide_index];
                });
            });
            updateRouteProgress();
            try {
                localStorage.setItem("toeic_answered_questions", JSON.stringify(state.answeredQuestions));
            } catch (e) {}
            
            renderPracticeSetsP4(sets, section);
        });
        
        document.getElementById("btn-set-review").addEventListener("click", () => {
            state.setQuiz.reviewMode = true;
            renderPracticeSetsP4(sets, section);
        });
    }

    function renderPracticeSetsReviewP4(sets, section) {
        practiceContentAreaP4.innerHTML = "";
        practiceContentAreaP4.style.maxWidth = "1000px";
        practiceContentAreaP4.style.margin = "0 auto";
        
        const reviewHeader = document.createElement("div");
        reviewHeader.className = "quiz-progress-header";
        reviewHeader.style.display = "flex";
        reviewHeader.style.justifyContent = "space-between";
        reviewHeader.style.alignItems = "center";
        reviewHeader.style.marginBottom = "24px";
        reviewHeader.style.padding = "14px 20px";
        reviewHeader.style.background = "rgba(255, 255, 255, 0.015)";
        reviewHeader.style.border = "1px solid var(--border)";
        
        const reviewTitle = document.createElement("span");
        reviewTitle.style.fontWeight = "700";
        reviewTitle.style.fontSize = "0.9rem";
        reviewTitle.textContent = "XEM LẠI CÁC ĐOẠN HỘI THOẠI & TRANSCRIPTS";
        
        const backBtn = document.createElement("button");
        backBtn.className = "mini-btn";
        backBtn.style.padding = "6px 12px";
        backBtn.textContent = "QUAY LẠI TỔNG KẾT";
        backBtn.style.borderRadius = "0px !important";
        backBtn.addEventListener("click", () => {
            state.setQuiz.currentIdx = sets.length; // triggers summary
            renderPracticeSetsP4(sets, section);
        });
        
        reviewHeader.appendChild(reviewTitle);
        reviewHeader.appendChild(backBtn);
        practiceContentAreaP4.appendChild(reviewHeader);

        sets.forEach(set => {
            const setWrapper = document.createElement("div");
            setWrapper.className = "practice-set-card";
            setWrapper.style.padding = "24px";
            setWrapper.style.marginBottom = "28px";
            setWrapper.style.border = "1px solid var(--border)";
            setWrapper.style.background = "rgba(255, 255, 255, 0.01)";
            
            const setHeader = document.createElement("h3");
            setHeader.style.fontSize = "1.15rem";
            setHeader.style.marginBottom = "16px";
            setHeader.style.fontWeight = "800";
            setHeader.textContent = `ĐOẠN HỘI THOẠI ${set.set_index}`;
            setWrapper.appendChild(setHeader);
            
            const audioDiv = document.createElement("div");
            setWrapper.appendChild(audioDiv);
            createAudioPlayer(set.audio, audioDiv);
            
            if (set.image) {
                const imgDiv = document.createElement("div");
                imgDiv.style.textAlign = "center";
                imgDiv.style.marginTop = "20px";
                imgDiv.style.marginBottom = "20px";
                imgDiv.innerHTML = `<img src="data/graphics/part04/${set.image}" alt="Graphic for Set ${set.set_index}" style="max-width: 100%; max-height: 400px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">`;
                setWrapper.appendChild(imgDiv);
            }
            
            const qListDiv = document.createElement("div");
            setWrapper.appendChild(qListDiv);
            
            set.questions.forEach(q => {
                const qCard = document.createElement("div");
                qCard.className = "question-block";
                qCard.style.padding = "20px";
                qCard.style.marginTop = "16px";
                
                const savedAns = state.setQuiz.answers[q.slide_index];
                const choicesHtml = renderChoicesHtml(q, true, savedAns);
                
                let badgeText = savedAns === q.answer ? 
                    `<span style="color: var(--success); margin-left: 10px; font-size: 0.85rem; font-weight: 700;">✔️ ĐÚNG</span>` : 
                    `<span style="color: var(--danger); margin-left: 10px; font-size: 0.85rem; font-weight: 700;">❌ SAI (Chọn ${savedAns || "Trống"})</span>`;
                
                const questionTextHtml = renderQuestionTextHtml(q, `rev-set-q-${q.slide_index}`, `<strong>QUESTION ${q.id}:</strong> `);
                
                qCard.innerHTML = `
                    <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom: 10px; width:100%;">
                        <div style="flex:1;">${questionTextHtml}</div>
                        <div>${badgeText}</div>
                    </div>
                    <div class="choices-stack" style="margin-top: 12px;">
                        ${choicesHtml}
                    </div>
                `;
                qListDiv.appendChild(qCard);
            });
            
            let explanationHtml = "";
            set.questions.forEach(sq => {
                if (sq.explanation) {
                    explanationHtml += `
                        <div class="explanation-box" style="margin-bottom: 16px; padding: 14px 18px; border: 1px solid var(--border); border-left: 4px solid var(--color-blue); background: rgba(59, 130, 246, 0.015);">
                            <h5 style="color: var(--color-blue); margin: 0 0 8px 0; font-size: 0.95rem; font-weight: 800; text-transform: uppercase;">
                                Giải thích QUESTION ${sq.id}:
                            </h5>
                            <div style="font-size: 0.9rem; line-height: 1.5; color: var(--text-main);">
                                ${sq.explanation}
                            </div>
                        </div>
                    `;
                }
            });
            
            const transcriptHtml = renderTranscriptHtml(set.transcript, set.vietnamese_transcript);
            const scriptCard = document.createElement("div");
            scriptCard.innerHTML = renderScriptCardHtml(`revset-${set.set_index}`, transcriptHtml, explanationHtml);
            const innerScriptCard = scriptCard.firstElementChild;
            innerScriptCard.classList.remove("hidden");
            
            setWrapper.appendChild(innerScriptCard);
            hookScriptCardToggler(`revset-${set.set_index}`);
            
            practiceContentAreaP4.appendChild(setWrapper);
        });
    }

    /* -------------------------------------------------------------
       7. LIGHT / DARK THEME TOGGLE
       ------------------------------------------------------------- */
    const savedTheme = localStorage.getItem("theme") || "dark";
    

    function setTheme(theme) {
        if (theme === "light") {
            document.body.classList.remove("dark-mode");
            document.body.classList.add("light-mode");
            themeIcon.innerHTML = `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>`;
            themeText.textContent = "TẮT ĐÈN";
            localStorage.setItem("theme", "light");
        } else {
            document.body.classList.add("dark-mode");
            document.body.classList.remove("light-mode");
            themeIcon.innerHTML = `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>`;
            themeText.textContent = "BẬT ĐÈN";
            localStorage.setItem("theme", "dark");
        }
    }
    
    setTheme(savedTheme);
    
    themeToggleBtn.addEventListener("click", () => {
        if (document.body.classList.contains("dark-mode")) {
            setTheme("light");
        } else {
            setTheme("dark");
        }
    });

    /* -------------------------------------------------------------
       8. NAME ENTRY SCREEN OVERLAY
       ------------------------------------------------------------- */
    const nameEntryOverlay = document.getElementById("nameEntryOverlay");
    const studentNameInput = document.getElementById("studentNameInput");
    const nameInputError = document.getElementById("nameInputError");
    const startLearningBtn = document.getElementById("startLearningBtn");
    const sidebarProfileBox = document.getElementById("sidebarProfileBox");
    const sidebarStudentName = document.getElementById("sidebarStudentName");
    const profileAvatar = document.getElementById("profileAvatar");
    const changeNameBtn = document.getElementById("changeNameBtn");
    const resetProgressBtn = document.getElementById("resetProgressBtn");

    function logStudentEntry(name) {
        if (!name) return;
        if (sessionStorage.getItem("loggedSession")) return;
        
        const formUrl = "https://docs.google.com/forms/d/e/1FAIpQLScMDz61SBJEcmXRUNwSZQVG0sr0dJFktmScdo0o4pfFL5yKNQ/formResponse";
        const formData = new URLSearchParams();
        formData.append("entry.388968236", name);
        
        fetch(formUrl, {
            method: "POST",
            mode: "no-cors",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: formData.toString()
        }).then(() => {
            sessionStorage.setItem("loggedSession", "true");
        }).catch(err => {
            console.warn("Google Form logging failed:", err);
            sessionStorage.setItem("loggedSession", "true");
        });
    }

    function checkStudentName() {
        const name = localStorage.getItem("studentName");
        if (!name) {
            nameEntryOverlay.style.display = "flex";
            nameEntryOverlay.style.opacity = "1";
            sidebarProfileBox.style.display = "none";
        } else {
            nameEntryOverlay.style.display = "none";
            sidebarProfileBox.style.display = "flex";
            sidebarStudentName.textContent = name.toUpperCase();
            profileAvatar.textContent = name.trim().charAt(0).toUpperCase();
            logStudentEntry(name);
        }
    }

    startLearningBtn.addEventListener("click", () => {
        const name = studentNameInput.value.trim();
        if (!name) {
            nameInputError.style.display = "block";
            studentNameInput.classList.add("shake");
            setTimeout(() => {
                studentNameInput.classList.remove("shake");
            }, 400);
        } else {
            const oldName = localStorage.getItem("studentName");
            if (oldName !== name) {
                sessionStorage.removeItem("loggedSession");
            }
            localStorage.setItem("studentName", name);
            nameInputError.style.display = "none";
            nameEntryOverlay.style.opacity = "0";
            setTimeout(() => {
                nameEntryOverlay.style.display = "none";
            }, 500);
            
            sidebarProfileBox.style.display = "flex";
            sidebarStudentName.textContent = name.toUpperCase();
            profileAvatar.textContent = name.charAt(0).toUpperCase();
            logStudentEntry(name);
        }
    });

    studentNameInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            startLearningBtn.click();
        }
    });

    changeNameBtn.addEventListener("click", () => {
        const currentName = localStorage.getItem("studentName") || "";
        studentNameInput.value = currentName;
        nameInputError.style.display = "none";
        nameEntryOverlay.style.display = "flex";
        setTimeout(() => {
            nameEntryOverlay.style.opacity = "1";
        }, 10);
        studentNameInput.focus();
    });

    if (resetProgressBtn) {
        resetProgressBtn.addEventListener("click", () => {
            if (confirm("Bạn có chắc chắn muốn xóa toàn bộ lịch sử làm bài? Dữ liệu không thể khôi phục sau khi xóa.")) {
                localStorage.removeItem("toeic_answered_questions");
                location.reload();
            }
        });
    }

    // Global Event Delegate for answered choice translations (Inspired by 'luyen-nghe-chong-diec' mechanics)
    document.addEventListener("click", (e) => {
        const optionBtn = e.target.closest(".choice-option");
        if (optionBtn && optionBtn.classList.contains("checked-done")) {
            const trans = optionBtn.querySelector(".c-trans");
            if (trans) {
                trans.style.display = trans.style.display === "block" ? "none" : "block";
            }
            e.stopPropagation();
        }
    });

    // Clear student name on reload to force re-entry (F5)
    localStorage.removeItem("studentName");
    checkStudentName();

    // Initialize default view state
    switchView(state.activeView);
});