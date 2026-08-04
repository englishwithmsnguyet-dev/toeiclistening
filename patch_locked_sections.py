import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_locked_sections = """    const LOCKED_SECTIONS = [
        "topic_01", "topic_02", "topic_03", "topic_04", "topic_05", "topic_06",
        "dang_02", "dang_03"
    ];"""

new_locked_sections = """    const LOCKED_SECTIONS = [
        "topic_01", "topic_02", "topic_03", "topic_04", "topic_05", "topic_06",
        "dang_02", "dang_03", "test_01", "test_02", "test_03", "test_04", "test_05"
    ];"""

js = js.replace(old_locked_sections, new_locked_sections)

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Added test sections to LOCKED_SECTIONS!")

