import sys

with open('js/app.js', 'r') as f:
    code = f.read()

# 3. Add togglePart1Submenu
p1_toggle = '''
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
'''
if 'function togglePart1Submenu' not in code:
    code = code.replace('function togglePart3Submenu', p1_toggle + '\n    function togglePart3Submenu')

# 4. In switchView
p1_switch = '''
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
'''
if 'viewName === "part1"' not in code:
    code = code.replace('} else if (viewName === "part3") {', p1_switch + '        } else if (viewName === "part3") {')

# 5. Nav click listener
p1_click = '''
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
'''
if 'navPart1Btn.addEventListener' not in code:
    code = code.replace('navPart2Btn.addEventListener("click", () => switchView("part2"));', p1_click + '\n    navPart2Btn.addEventListener("click", () => switchView("part2"));')

# Hide part 1 submenu when clicking part 3/4
code = code.replace('togglePart3Submenu(false);\n            togglePart4Submenu(false);', 'if (typeof togglePart1Submenu !== "undefined") togglePart1Submenu(false);\n            togglePart3Submenu(false);\n            togglePart4Submenu(false);')
code = code.replace('togglePart4Submenu(true);', 'if (typeof togglePart1Submenu !== "undefined") togglePart1Submenu(false);\n            togglePart4Submenu(true);')
code = code.replace('togglePart3Submenu(true);', 'if (typeof togglePart1Submenu !== "undefined") togglePart1Submenu(false);\n            togglePart3Submenu(true);')

with open('js/app.js', 'w') as f:
    f.write(code)
print('Patch 2 done.')
