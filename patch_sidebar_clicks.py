import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix initializePart01Sidebar
old_p1_click = """                    if (LOCKED_SECTIONS.includes(node.id) && !isUnlocked) {
                        showPaywallModal();
                        return;
                    }"""
new_p1_click = """                    if (LOCKED_SECTIONS.includes(node.id) && !window.isUnlocked) {
                        window.showPaywallModal(() => loadSectionP1(node.id));
                        return;
                    }"""
js = js.replace(old_p1_click, new_p1_click)

old_p1_test_click = """                        if (LOCKED_SECTIONS.includes(section.id) && !isUnlocked) {
                            showPaywallModal();
                            return;
                        }"""
new_p1_test_click = """                        if (LOCKED_SECTIONS.includes(section.id) && !window.isUnlocked) {
                            window.showPaywallModal(() => loadSectionP1(section.id));
                            return;
                        }"""
js = js.replace(old_p1_test_click, new_p1_test_click)

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Fixed sidebar click callbacks!")
