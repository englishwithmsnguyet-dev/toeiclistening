import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_card2 = """    const cardPart2 = document.getElementById("card-part2");
    if (cardPart2) {
        cardPart2.addEventListener("click", () => switchView("part2"));
    }"""

new_card2 = """    const cardPart1 = document.getElementById("card-part1");
    if (cardPart1) {
        cardPart1.addEventListener("click", () => switchView("part1"));
    }
    
    const cardPart2 = document.getElementById("card-part2");
    if (cardPart2) {
        cardPart2.addEventListener("click", () => switchView("part2"));
    }"""

js = js.replace(old_card2, new_card2)

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Added cardPart1 event listener!")
