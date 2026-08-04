import re

with open("js/app.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if "function loadSection(id)" in line:
        start_idx = i
    if "function setTheme(theme)" in line:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    block = "".join(lines[start_idx:end_idx])
    
    # Replace part 3 variables with part 4
    block_p4 = block.replace("part03Data", "part04Data")
    block_p4 = block_p4.replace("part03ActiveSection", "part04ActiveSection")
    block_p4 = block_p4.replace("part03ActiveTab", "part04ActiveTab")
    block_p4 = block_p4.replace("loadSection", "loadSectionP4")
    block_p4 = block_p4.replace("renderPanelTab", "renderPanelTabP4")
    block_p4 = block_p4.replace("switchView(\"part3\")", "switchView(\"part4\")")
    block_p4 = block_p4.replace("state.activeView !== \"part3\"", "state.activeView !== \"part4\"")
    
    # DOM variables
    dom_vars = [
        "breadParent", "breadCurrent", "panelTitle",
        "secBtnTheory", "secBtnVocabulary", "secBtnExamples", "secBtnPractice",
        "secTheory", "secVocabulary", "secExamples", "secPractice",
        "theoryContentArea", "vocabularyContentArea", "examplesContentArea", "practiceContentArea"
    ]
    
    for var in dom_vars:
        block_p4 = re.sub(r'\b' + var + r'\b', var + "P4", block_p4)
        
    block_p4 = block_p4.replace("part3SubmenuContainer", "part4SubmenuContainer")
    block_p4 = block_p4.replace("part3ExpandIcon", "part4ExpandIcon")
    
    block_p4 = block_p4.replace("`sec-${tabName}`", "`sec-${tabName}-p4`")
    
    lines.insert(end_idx, "\n// ================= PART 04 FUNCTIONS =================\n\n" + block_p4 + "\n")
    
    with open("js/app.js", "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("Successfully patched js/app.js with P4 functions!")
else:
    print("Could not find start or end index.")
