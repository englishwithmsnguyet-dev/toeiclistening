import re

app_path = "js/app.js"
with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

funcs = [
    "renderTheory", "renderVocabulary", "renderExamples", "renderPractice",
    "renderPracticeQuestions", "renderPracticeQuestionsSummary", "renderPracticeQuestionsReview",
    "renderPracticeSets", "renderPracticeSetsSummary", "renderPracticeSetsReview",
    "renderPanelTab"
]

dom_vars = [
    "panelTitle", "secBtnTheory", "secBtnVocabulary", "secBtnExamples", "secBtnPractice",
    "secTheory", "secVocabulary", "secExamples", "secPractice",
    "theoryContentArea", "vocabularyContentArea", "examplesContentArea", "practiceContentArea",
    "breadParent", "breadCurrent"
]

def extract_function(content, func_name):
    start = content.find(f"function {func_name}(")
    if start == -1: return ""
    brace_count = 0
    idx = start
    while idx < len(content):
        if content[idx] == "{":
            brace_count += 1
        elif content[idx] == "}":
            brace_count -= 1
            if brace_count == 0:
                return content[start:idx+1]
        idx += 1
    return ""

for func in funcs:
    body = extract_function(content, func)
    found_globals = []
    for var in dom_vars:
        if re.search(r'\b' + var + r'\b', body):
            found_globals.append(var)
    if found_globals:
        print(f"{func} uses {found_globals}")
