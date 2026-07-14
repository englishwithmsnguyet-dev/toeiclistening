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
        "topic_01", "topic_02", "topic_03", "topic_04", "topic_05", "topic_06"
    ];

    // App State
    const state = {
        activeView: "home",
        part03Data: null,
        part03ActiveSection: "overview", // Active category ID (e.g. 'overview', 'dang_01_topic')
        part03ActiveTab: "theory", // 'theory', 'vocabulary', 'examples', 'practice'
        
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
    
    const contentViews = document.querySelectorAll(".content-view");
    const mainTitleText = document.getElementById("main-title-text");

    // Part 2 elements
    const part02SlideImg = document.getElementById("part02-slide");
    const part02CurrentText = document.getElementById("slide-current");
    const part02PrevBtn = document.getElementById("slide-prev");
    const part02NextBtn = document.getElementById("slide-next");
    const part02GoInput = document.getElementById("goto-slide-input");
    const part02GoBtn = document.getElementById("goto-slide-btn");
    const part02Spinner = document.getElementById("slide-spinner");

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
    function togglePart3Submenu(expand) {
        if (expand) {
            part3SubmenuContainer.style.display = "block";
            part3ExpandIcon.innerHTML = icons.chevronUp;
        } else {
            part3SubmenuContainer.style.display = "none";
            part3ExpandIcon.innerHTML = icons.chevronDown;
        }
    }

    function switchView(viewName) {
        state.activeView = viewName;
        stopAudio();
        
        // Update sidebar highlights
        if (viewName === "home") {
            navHomeBtn.classList.add("active");
            navPart2Btn.classList.remove("active");
            navPart3Btn.classList.remove("active");
            document.querySelectorAll(".submenu-item").forEach(item => item.classList.remove("active"));
            togglePart3Submenu(false);
        } else if (viewName === "part2") {
            navHomeBtn.classList.remove("active");
            navPart2Btn.classList.add("active");
            navPart3Btn.classList.remove("active");
            document.querySelectorAll(".submenu-item").forEach(item => item.classList.remove("active"));
            loadPart02Slide(state.part02CurrentSlide);
            togglePart3Submenu(false);
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
            togglePart3Submenu(true);
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
        } else if (viewName === "part3") {
            mainTitleText.textContent = "PART 03: SHORT CONVERSATIONS";
        }
    }
    
    navHomeBtn.addEventListener("click", () => switchView("home"));
    navPart2Btn.addEventListener("click", () => switchView("part2"));
    
    navPart3Btn.addEventListener("click", () => {
        if (state.activeView === "part3") {
            const isVisible = part3SubmenuContainer.style.display === "block";
            togglePart3Submenu(!isVisible);
        } else {
            loadSection(state.part03ActiveSection || "overview");
        }
    });
    
    // Quick triggers from Dashboard
    const cardPart3 = document.getElementById("card-part3");
    if (cardPart3) {
        cardPart3.addEventListener("click", () => loadSection("overview"));
    }
    const cardPart2 = document.getElementById("card-part2");
    if (cardPart2) {
        cardPart2.addEventListener("click", () => switchView("part2"));
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
       3. PART 02: SLIDE CAROUSEL
       ------------------------------------------------------------- */
    function loadPart02Slide(index) {
        if (index < 1) index = 1;
        if (index > state.part02TotalSlides) index = state.part02TotalSlides;
        
        state.part02CurrentSlide = index;
        part02CurrentText.textContent = index;
        part02GoInput.value = index;
        
        part02Spinner.style.display = "block";
        part02SlideImg.src = `../TOEIC LISTENING - PART 02/Slide${index}.png`;
        
        part02SlideImg.onload = () => {
            part02Spinner.style.display = "none";
        };
        part02SlideImg.onerror = () => {
            part02Spinner.style.display = "none";
            part02SlideImg.alt = `Không thể tải Slide ${index} (Vui lòng kiểm tra thư mục Slide)`;
        };
    }
    
    if (part02PrevBtn) {
        part02PrevBtn.addEventListener("click", () => {
            loadPart02Slide(state.part02CurrentSlide - 1);
        });
    }
    if (part02NextBtn) {
        part02NextBtn.addEventListener("click", () => {
            loadPart02Slide(state.part02CurrentSlide + 1);
        });
    }
    if (part02GoBtn) {
        part02GoBtn.addEventListener("click", () => {
            const index = parseInt(part02GoInput.value, 10);
            if (!isNaN(index)) loadPart02Slide(index);
        });
    }
    if (part02GoInput) {
        part02GoInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                const index = parseInt(part02GoInput.value, 10);
                if (!isNaN(index)) loadPart02Slide(index);
            }
        });
    }

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
            let cleanVal = val.replace(/<[^>]+>/g, "").trim();
            let labelRegex = new RegExp("^" + k + "\\s*\\.\\s*", "i");
            if (!labelRegex.test(cleanVal)) {
                parts.push(k + ". " + val);
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
        
        const isUnlocked = sessionStorage.getItem("portal_unlocked") === "true";
        
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
            if (item.type === "topic") {
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

    function loadSection(id) {
        const isUnlocked = sessionStorage.getItem("portal_unlocked") === "true";
        if (LOCKED_SECTIONS.includes(id) && !isUnlocked) {
            const pass = prompt("Phần này đang khóa. Vui lòng nhập mật khẩu để mở khóa:");
            if (pass === "missnguyet2026") {
                sessionStorage.setItem("portal_unlocked", "true");
                alert("Mở khóa thành công!");
                initializePart03Sidebar(); // Refresh sidebar to remove locks
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
        } else if (section.type === "topic") {
            parentText = "Chủ đề nghe";
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
        if (qText && (qText.includes("PRACTICE") || qText.includes("Example") || qText.includes("EXAMPLE"))) {
            textPrefix = "";
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
                <div class="question-text">${textPrefix}${qText}</div>
                ${graphicHtml}
            `;
        }
        
        return `
            <div class="question-text-wrapper" style="cursor: pointer; width: 100%;" onclick="const t = this.querySelector('.q-trans'); t.style.display = t.style.display === 'block' ? 'none' : 'block'; event.stopPropagation();" title="Click vào câu hỏi để xem dịch nghĩa">
                <div class="question-text" style="margin-bottom: 6px; text-align: left; width: 100%;">
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
                const cleanViet = lineViet.replace(/^[A-Za-z]+[-A-Za-z]*\s*:\s*/, "");
                transHtml = `<div class="line-trans-text" style="color: var(--text-muted); font-size: 0.88rem; font-style: italic; margin-top: 4px; border-left: 2px solid var(--border); padding-left: 8px;">${cleanViet}</div>`;
            }
            html += `
                <div class="transcript-line-wrapper" style="margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px dashed var(--border); text-align: left;">
                    <p class="transcript-line" style="margin: 0; font-weight: 500; line-height: 1.5;">${line}</p>
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
        const revHeader = document.getElementById(`header-reveal-${idLabel}`);
        const revContent = document.getElementById(`reveal-content-${idLabel}`);
        if (revHeader && revContent) {
            revHeader.addEventListener("click", () => {
                revContent.classList.toggle("open");
                if (revContent.classList.contains("open")) {
                    revHeader.querySelector("svg").outerHTML = icons.chevronUp;
                } else {
                    revHeader.querySelector("svg").outerHTML = icons.chevronDown;
                }
            });
        }
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
                <div class="dashboard-hero" style="background: linear-gradient(135deg, #1e1b4b 0%, #312e81 60%, #4361ee 100%); color: white; padding: 40px; margin-bottom: 30px; border-left: 5px solid var(--color-cyan); border-radius: 0px !important;">
                    <span style="display: inline-block; background: rgba(0, 242, 254, 0.15); color: var(--color-cyan); padding: 4px 12px; font-size: 0.75rem; font-weight: 700; margin-bottom: 12px; border: 1px solid rgba(0, 242, 254, 0.3); text-transform: uppercase; letter-spacing: 0.05em;">Part 03: Short Conversations</span>
                    <h2 style="font-size: 2.2rem; font-weight: 800; color: white; margin-bottom: 10px;">TỔNG QUAN NỘI DUNG PHẦN 03</h2>
                    <p style="color: rgba(255,255,255,0.8); font-size: 1.05rem; line-height: 1.6; max-width: 700px; margin: 0 0 25px 0;">Học cách nghe hiểu các cuộc đối thoại ngắn, nắm bắt từ khóa và phản xạ chọn đáp án nhanh chóng trong bài nghe.</p>
                    
                    <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-top: 15px;">
                        <div style="background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.12); padding: 12px 20px; display: flex; align-items: center; gap: 12px;">
                            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="var(--color-cyan)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                            <div>
                                <strong style="font-size: 1.15rem; display: block; color: white; line-height: 1.2;">39 Câu Hỏi</strong>
                                <span style="font-size: 0.75rem; color: rgba(255,255,255,0.6);">Từ câu 32 đến câu 70</span>
                            </div>
                        </div>
                        <div style="background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.12); padding: 12px 20px; display: flex; align-items: center; gap: 12px;">
                            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="var(--color-cyan)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
                            <div>
                                <strong style="font-size: 1.15rem; display: block; color: white; line-height: 1.2;">13 Đoạn Thoại</strong>
                                <span style="font-size: 0.75rem; color: rgba(255,255,255,0.6);">Cuộc trò chuyện ngắn</span>
                            </div>
                        </div>
                        <div style="background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.12); padding: 12px 20px; display: flex; align-items: center; gap: 12px;">
                            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="var(--color-cyan)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                            <div>
                                <strong style="font-size: 1.15rem; display: block; color: white; line-height: 1.2;">2 - 3 Người</strong>
                                <span style="font-size: 0.75rem; color: rgba(255,255,255,0.6);">Số lượng người nói</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div style="font-size: 1.25rem; font-weight: 800; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; color: var(--color-cyan); text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid var(--border); padding-bottom: 8px;">
                    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle;"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="9" y1="9" x2="15" y2="9"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="15" y2="17"/></svg> CẤU TRÚC VÀ CÁC QUY TẮC TRỌNG TÂM
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 30px;">
                    <div style="background: var(--bg-card); border: 1px solid var(--border); padding: 25px; transition: border-color 0.2s; border-radius: 0px !important;">
                        <div style="width: 44px; height: 44px; background: rgba(0, 242, 254, 0.08); color: var(--color-cyan); display: flex; align-items: center; justify-content: center; font-size: 1.25rem; margin-bottom: 15px; border: 1px solid rgba(0, 242, 254, 0.2);"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></div>
                        <h4 style="font-size: 1.1rem; font-weight: 800; color: var(--text-main); margin-bottom: 8px;">13 Đoạn Hội Thoại</h4>
                        <p style="font-size: 0.95rem; color: var(--text-muted); line-height: 1.6; margin: 0;">Mỗi đoạn hội thoại gồm 03 câu hỏi đi kèm. Nội dung thường xoay quanh các tình huống trong công việc và đời sống hàng ngày như họp hành, mua sắm, dịch vụ...</p>
                    </div>

                    <div style="background: var(--bg-card); border: 1px solid var(--border); padding: 25px; transition: border-color 0.2s; border-radius: 0px !important;">
                        <div style="width: 44px; height: 44px; background: rgba(0, 242, 254, 0.08); color: var(--color-cyan); display: flex; align-items: center; justify-content: center; font-size: 1.25rem; margin-bottom: 15px; border: 1px solid rgba(0, 242, 254, 0.2);"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a5 5 0 0 0-5 5v3.18a3 3 0 0 0-.58 1.7l1 5A3 3 0 0 0 10.38 18h3.24a3 3 0 0 0 3-2.12l1-5a3 3 0 0 0-.58-1.7V6a5 5 0 0 0-5-5z"/></svg></div>
                        <h4 style="font-size: 1.1rem; font-weight: 800; color: var(--text-main); margin-bottom: 8px;">Chỉ Được Nghe 1 Lần</h4>
                        <p style="font-size: 0.95rem; color: var(--text-muted); line-height: 1.6; margin: 0;">Thí sinh không được nghe lại lần thứ hai. Hãy tập trung cao độ ngay khi âm thanh bắt đầu phát và không phân tâm khi bỏ lỡ từ khóa.</p>
                    </div>

                    <div style="background: var(--bg-card); border: 1px solid var(--border); padding: 25px; transition: border-color 0.2s; border-radius: 0px !important;">
                        <div style="width: 44px; height: 44px; background: rgba(0, 242, 254, 0.08); color: var(--color-cyan); display: flex; align-items: center; justify-content: center; font-size: 1.25rem; margin-bottom: 15px; border: 1px solid rgba(0, 242, 254, 0.2);"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div>
                        <h4 style="font-size: 1.1rem; font-weight: 800; color: var(--text-main); margin-bottom: 8px;">Tận Dụng Thời Gian Chờ</h4>
                        <p style="font-size: 0.95rem; color: var(--text-muted); line-height: 1.6; margin: 0;">Trong khi băng đọc câu hỏi, hãy tranh thủ đánh dấu đáp án và <strong>đọc trước bộ câu hỏi tiếp theo</strong> để dự đoán nội dung hội thoại sắp nghe.</p>
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
                    <h3 style="font-size: 1.35rem; font-weight: 700; color: var(--color-cyan); margin: 0 0 24px 0; text-transform: uppercase; border-left: 4px solid var(--color-purple); padding-left: 14px; line-height: 1.4;">
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
                const htmlBulletRegex = /^((?:<[^>]+>\s*)*)(?:•|o|-|\*|◦)\s+/i;
                
                if (htmlBulletRegex.test(cleanLine)) {
                    const cleanedHtml = cleanLine.replace(htmlBulletRegex, "$1").trim();
                    docHtml += `
                        <div class="theory-bullet" style="margin-bottom: 12px;">
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
        
        if (section.type === "topic") {
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
                            <div class="explanation-box" style="margin-bottom: 16px; padding: 14px 18px; border: 1px solid var(--border); border-left: 4px solid var(--color-cyan); background: rgba(0, 242, 254, 0.01);">
                                <h5 style="color: var(--color-cyan); margin: 0 0 8px 0; font-size: 0.95rem; font-weight: 800; text-transform: uppercase;">
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
                        <div class="explanation-box" style="margin-bottom: 16px; padding: 14px 18px; border: 1px solid var(--border); border-left: 4px solid var(--color-cyan); background: rgba(0, 242, 254, 0.01);">
                            <h5 style="color: var(--color-cyan); margin: 0 0 8px 0; font-size: 0.95rem; font-weight: 800; text-transform: uppercase;">
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
        } else if (section.type === "topic") {
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
                <div class="explanation-box" style="margin-bottom: 16px; padding: 14px 18px; border: 1px solid var(--border); border-left: 4px solid var(--color-cyan); background: rgba(0, 242, 254, 0.01);">
                    <h5 style="color: var(--color-cyan); margin: 0 0 8px 0; font-size: 0.95rem; font-weight: 800; text-transform: uppercase;">
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
            <div style="font-size: 2.8rem; font-weight: 800; color: var(--color-cyan); margin-bottom: 16px;">
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
                    <div class="explanation-box" style="margin-bottom: 16px; padding: 14px 18px; border: 1px solid var(--border); border-left: 4px solid var(--color-cyan); background: rgba(0, 242, 254, 0.01);">
                        <h5 style="color: var(--color-cyan); margin: 0 0 8px 0; font-size: 0.95rem; font-weight: 800; text-transform: uppercase;">
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
        if (!sets || sets.length === 0) {
            practiceContentArea.innerHTML = "<p style='color: var(--text-muted); font-weight: 700;'>Bài tập đang được cập nhật.</p>";
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
            renderPracticeSetsReview(sets, section);
            return;
        }

        const currentIdx = state.setQuiz.currentIdx;
        
        if (currentIdx >= sets.length) {
            renderPracticeSetsSummary(sets, section);
            return;
        }

        const set = sets[currentIdx];
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
        progressText.textContent = `ĐOẠN HỘI THOẠI ${currentIdx + 1} / ${sets.length}`;
        
        const completedCount = Object.keys(state.setQuiz.completedSets).length;
        const progressScore = document.createElement("span");
        progressScore.style.fontWeight = "800";
        progressScore.style.fontSize = "0.95rem";
        progressScore.style.color = "var(--color-cyan)";
        progressScore.textContent = `HOÀN THÀNH: ${completedCount} / ${sets.length}`;
        
        progressHeader.appendChild(progressText);
        progressHeader.appendChild(progressScore);
        practiceContentArea.appendChild(progressHeader);

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
        
        const scoreSpan = document.createElement("span");
        scoreSpan.className = "score-display";
        scoreSpan.style.fontWeight = "800";
        scoreSpan.style.fontSize = "1.05rem";
        scoreSpan.style.color = "var(--color-cyan)";
        
        const submitBtn = document.createElement("button");
        submitBtn.className = "action-btn btn-primary";
        submitBtn.style.padding = "12px 24px";
        submitBtn.textContent = "NỘP BÀI TRẢ LỜI";
        submitBtn.disabled = true;
        submitBtn.style.borderRadius = "0px !important";
        
        const nextBtn = document.createElement("button");
        nextBtn.className = "action-btn btn-primary";
        nextBtn.style.padding = "12px 24px";
        nextBtn.style.display = "none";
        nextBtn.textContent = "ĐOẠN TIẾP THEO";
        nextBtn.style.borderRadius = "0px !important";
        
        if (setAlreadySubmitted) {
            const score = state.setQuiz.completedSets[set.set_index];
            scoreSpan.textContent = `Kết quả: ${score} / ${set.questions.length} câu đúng`;
            submitBtn.style.display = "none";
            nextBtn.style.display = "flex";
        } else {
            submitRow.appendChild(scoreSpan);
            submitRow.appendChild(submitBtn);
        }
        submitRow.appendChild(nextBtn);
        setWrapper.appendChild(submitRow);
        
        // Transcript & Explanations Card
        let explanationHtml = "";
        set.questions.forEach(sq => {
            if (sq.explanation) {
                explanationHtml += `
                    <div class="explanation-box" style="margin-bottom: 16px; padding: 14px 18px; border: 1px solid var(--border); border-left: 4px solid var(--color-cyan); background: rgba(0, 242, 254, 0.01);">
                        <h5 style="color: var(--color-cyan); margin: 0 0 8px 0; font-size: 0.95rem; font-weight: 800; text-transform: uppercase;">
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
                });
                
                if (userVal === correctVal) {
                    correctCount++;
                }
                
                markQuestionAnswered(q.slide_index);
            });
            
            state.setQuiz.completedSets[set.set_index] = correctCount;
            
            scoreSpan.textContent = `Kết quả: ${correctCount} / ${numQs} câu đúng`;
            submitBtn.style.display = "none";
            nextBtn.style.display = "flex";
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
            renderPracticeSets(sets, section);
        });
        
        practiceContentArea.appendChild(setWrapper);
    }

    function renderPracticeSetsSummary(sets, section) {
        practiceContentArea.innerHTML = "";
        
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
            <div style="font-size: 2.8rem; font-weight: 800; color: var(--color-cyan); margin-bottom: 16px;">
                ${totalScore} / ${totalQs}
            </div>
            <p style="color: var(--text-muted); font-size: 1.05rem; margin-bottom: 36px; line-height: 1.7; max-width: 500px; margin-left: auto; margin-right: auto;">${msg}</p>
            <div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap;">
                <button class="btn btn-primary" id="btn-set-retry" style="padding: 12px 24px; font-weight: 700; border-radius: 0px !important;">LÀM LẠI TOÀN BỘ</button>
                <button class="btn btn-secondary" id="btn-set-review" style="padding: 12px 24px; font-weight: 700; border-radius: 0px !important;">XEM LẠI CÁC ĐÁP ÁN</button>
            </div>
        `;
        
        practiceContentArea.appendChild(summaryCard);
        
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
            
            renderPracticeSets(sets, section);
        });
        
        document.getElementById("btn-set-review").addEventListener("click", () => {
            state.setQuiz.reviewMode = true;
            renderPracticeSets(sets, section);
        });
    }

    function renderPracticeSetsReview(sets, section) {
        practiceContentArea.innerHTML = "";
        
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
            renderPracticeSets(sets, section);
        });
        
        reviewHeader.appendChild(reviewTitle);
        reviewHeader.appendChild(backBtn);
        practiceContentArea.appendChild(reviewHeader);

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
                        <div class="explanation-box" style="margin-bottom: 16px; padding: 14px 18px; border: 1px solid var(--border); border-left: 4px solid var(--color-cyan); background: rgba(0, 242, 254, 0.01);">
                            <h5 style="color: var(--color-cyan); margin: 0 0 8px 0; font-size: 0.95rem; font-weight: 800; text-transform: uppercase;">
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
            
            practiceContentArea.appendChild(setWrapper);
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
