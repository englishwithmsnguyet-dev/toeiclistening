import json

with open("data/part01_data.js", "r", encoding="utf-8") as f:
    content = f.read()

start_idx = content.find("[")
end_idx = content.rfind("]") + 1
data = json.loads(content[start_idx:end_idx])

# The mapping from slide_index to audio filename
audio_mapping = {
    48: "media42.mp3",
    49: "media42.mp3",
    50: "media43.mp3",
    51: "media43.mp3",
    52: "media44.mp3",
    53: "media44.mp3",
    54: "media45.mp3",
    55: "media45.mp3",
    56: "media46.mp3",
    57: "media46.mp3",
}

for section in data:
    if section.get("id") == "dang_03":
        for slide in section.get("theory", []):
            idx = slide.get("slide_index")
            if idx in audio_mapping:
                slide["audio"] = audio_mapping[idx]
                
                # Also replace any references inside the HTML text
                if "text" in slide and len(slide["text"]) > 0:
                    html = slide["text"][0]
                    # We know that the previous script injected playAudio('media42.mp3', event) everywhere
                    import re
                    # Replace playAudio('media*.mp3', ...) with the correct audio file
                    # We can simply replace 'media42.mp3' if it's there
                    html = re.sub(r"playAudio\('media42\.mp3'", f"playAudio('{audio_mapping[idx]}'", html)
                    slide["text"][0] = html

new_content = "window.part01Data = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n"
with open("data/part01_data.js", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Done fixing dang_03 practice audio.")
