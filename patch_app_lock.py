import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. We need to add the showPaywallModal function and password modal logic
# I will insert it right after `let isUnlocked = ...` or near the top where global state is.
# Wait, currently there is no `isUnlocked` global variable?
# Let's check `sessionStorage.getItem("portal_unlocked") === "true"` in app.js
if "window.isUnlocked = sessionStorage.getItem" not in js:
    # Find a good place to inject the global variables
    # Maybe right after `const state = { ... };`
    state_block = """    };

    // --- LOCK & PASSWORD LOGIC ---
    window.isUnlocked = sessionStorage.getItem("portal_unlocked") === "true";
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

    document.addEventListener("DOMContentLoaded", () => {
        const submitBtn = document.getElementById('submitPasswordBtn');
        const cancelBtn = document.getElementById('cancelPasswordBtn');
        const passInput = document.getElementById('passwordInput');
        
        if (submitBtn) {
            submitBtn.addEventListener('click', () => {
                if (passInput && passInput.value === "2026") {
                    window.isUnlocked = true;
                    sessionStorage.setItem("portal_unlocked", "true");
                    window.closePasswordModal();
                    if (window.pendingUnlockCallback) window.pendingUnlockCallback();
                    
                    // Refresh sidebars to remove lock icons
                    if (typeof initializePart01Sidebar === 'function') initializePart01Sidebar();
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
    });
    // --- END LOCK LOGIC ---
"""
    js = js.replace('    };\n\n    // Audio context initialization', state_block + '\n    // Audio context initialization')


# 2. Patch switchView to intercept part2, part3, part4
old_switchView = """    function switchView(viewName) {
        state.activeView = viewName;"""

new_switchView = """    function switchView(viewName) {
        if (!window.isUnlocked && (viewName === "part2" || viewName === "part3" || viewName === "part4")) {
            window.showPaywallModal(() => switchView(viewName));
            return;
        }
        state.activeView = viewName;"""

js = js.replace(old_switchView, new_switchView)


# 3. Patch LOCKED_SECTIONS to also include dang_02 and dang_03
# So `loadPart1Nav` will automatically lock them using the existing `LOCKED_SECTIONS.includes(node.id)` logic!
old_locked_sections = """    const LOCKED_SECTIONS = [
        "topic_01", "topic_02", "topic_03", "topic_04", "topic_05", "topic_06"
    ];"""

new_locked_sections = """    const LOCKED_SECTIONS = [
        "topic_01", "topic_02", "topic_03", "topic_04", "topic_05", "topic_06",
        "dang_02", "dang_03"
    ];"""

js = js.replace(old_locked_sections, new_locked_sections)

# 4. Replace `const isUnlocked = sessionStorage.getItem("portal_unlocked") === "true";` inside initialize functions 
# with `const isUnlocked = window.isUnlocked;` to ensure they use the global state.
js = js.replace('const isUnlocked = sessionStorage.getItem("portal_unlocked") === "true";', 'const isUnlocked = window.isUnlocked;')

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("app.js patched successfully!")

