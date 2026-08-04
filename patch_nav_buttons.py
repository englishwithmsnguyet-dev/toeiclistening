import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_part3 = """    navPart3Btn.addEventListener("click", () => {
        if (state.activeView === "part3") {
            const isVisible = part3SubmenuContainer.style.display === "block";
            togglePart3Submenu(!isVisible);
        } else {
            loadSection(state.part03ActiveSection || "overview");
        }
    });"""

new_part3 = """    navPart3Btn.addEventListener("click", () => {
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
    });"""

js = js.replace(old_part3, new_part3)

old_part4 = """    if (typeof navPart4Btn !== 'undefined' && navPart4Btn) {
        navPart4Btn.addEventListener("click", () => {
            if (state.activeView === "part4") {
                const isVisible = part4SubmenuContainer.style.display === "block";
                togglePart4Submenu(!isVisible);
            } else {
                loadSectionP4(state.part04ActiveSection || "overview");
            }
        });
    }"""

new_part4 = """    if (typeof navPart4Btn !== 'undefined' && navPart4Btn) {
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
    }"""

js = js.replace(old_part4, new_part4)

# Also fix loadSection and loadSectionP4 so they use showPaywallModal instead of native prompt just in case!
old_load_section_prompt = """            const pass = prompt("Phần này đang khóa. Vui lòng nhập mật khẩu để mở khóa:");
            if (pass === "missnguyet2026") {"""
new_load_section_prompt = """            window.showPaywallModal(() => loadSection(id));
            return;
            if (false) {"""
js = js.replace(old_load_section_prompt, new_load_section_prompt)

old_load_section_p4_prompt = """            const pass = prompt("Phần này đang khóa. Vui lòng nhập mật khẩu để mở khóa:");
            if (pass === "missnguyet2026") {"""
new_load_section_p4_prompt = """            window.showPaywallModal(() => loadSectionP4(id));
            return;
            if (false) {"""
js = js.replace(old_load_section_p4_prompt, new_load_section_p4_prompt)


with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated navPart3Btn and navPart4Btn!")
