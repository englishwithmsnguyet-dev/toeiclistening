import re

with open("js/app.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

start_cleanup = -1
end_cleanup = -1
start_sidebar = -1
end_sidebar = -1

for i, line in enumerate(lines):
    if "if (window.part03Data)" in line:
        start_cleanup = i
    if "function initializePart03Sidebar()" in line:
        end_cleanup = i 
        start_sidebar = i
    if "function loadSection(id)" in line:
        end_sidebar = i
        break

if start_cleanup != -1 and end_sidebar != -1:
    cleanup_block = "".join(lines[start_cleanup:end_cleanup])
    sidebar_block = "".join(lines[start_sidebar:end_sidebar])
    
    cleanup_p4 = cleanup_block.replace("03", "04").replace("part3", "part4")
    sidebar_p4 = sidebar_block.replace("03", "04").replace("part3", "part4").replace("loadSection", "loadSectionP4")
    
    lines.insert(end_sidebar, "\n" + cleanup_p4 + sidebar_p4)
    
    for i, line in enumerate(lines):
        if "initializePart03Sidebar();" in line and "function" not in line:
            lines[i] = line.replace("initializePart03Sidebar();", "initializePart03Sidebar();\n    initializePart04Sidebar();")
            
    with open("js/app.js", "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("Successfully patched data blocks!")
else:
    print("Could not find blocks.")
