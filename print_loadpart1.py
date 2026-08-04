with open('js/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_func = False
for line in lines:
    if "function loadPart1Nav" in line or "const loadPart1Nav =" in line:
        in_func = True
    if in_func:
        print(line, end='')
        if "function" in line and "{" in line and "}" in line and not "loadPart1Nav" in line:
            pass
        # Just print until "function initializePart02" or something
    if in_func and "function initialize" in line:
        break
