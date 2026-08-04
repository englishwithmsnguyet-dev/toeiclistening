import sys

with open('js/app.js', 'r') as f:
    code = f.read()

p1_init = '''
    function initializePart01Sidebar() {
        if (!part1ConceptsNavList || !part1TopicsNavList) return;
        
        part1ConceptsNavList.innerHTML = "";
        part1TopicsNavList.innerHTML = "";
        
        const isUnlocked = sessionStorage.getItem("portal_unlocked") === "true";
        
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
                    if (LOCKED_SECTIONS.includes(node.id) && !isUnlocked) {
                        showPaywallModal();
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
                        if (LOCKED_SECTIONS.includes(section.id) && !isUnlocked) {
                            showPaywallModal();
                            return;
                        }
                        loadSectionP1(section.id);
                    });
                    
                    part1TopicsNavList.appendChild(submenuItem);
                }
            });
        }
    }
'''

if 'function initializePart01Sidebar' not in code:
    code = code.replace('function initializePart04Sidebar() {', p1_init + '\n    function initializePart04Sidebar() {')

# Also initialize in checkLogin
code = code.replace('if (typeof initializePart04Sidebar !== "undefined") initializePart04Sidebar();', 'if (typeof initializePart01Sidebar !== "undefined") initializePart01Sidebar();\n            if (typeof initializePart04Sidebar !== "undefined") initializePart04Sidebar();')

with open('js/app.js', 'w') as f:
    f.write(code)
print('Patch 3 done.')
