with open('js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

def check_brackets(text):
    stack = []
    lines = text.split('\n')
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char in '{[(':
                stack.append((char, i+1))
            elif char in '}])':
                if not stack:
                    return f'Unmatched closing bracket {char} at line {i+1}'
                last_char, line_num = stack.pop()
                if (char == '}' and last_char != '{') or \
                   (char == ']' and last_char != '[') or \
                   (char == ')' and last_char != '('):
                    return f'Mismatched bracket {char} at line {i+1}, expected match for {last_char} at line {line_num}'
    if stack:
        return f'Unmatched opening bracket {stack[-1][0]} at line {stack[-1][1]}'
    return 'Brackets are balanced.'

import re
text = re.sub(r'//.*', '', text)
text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
print(check_brackets(text))
