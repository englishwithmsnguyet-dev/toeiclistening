import json

with open("data/part01_data.json", "r") as f:
    data = json.load(f)

for sec in data:
    if sec["type"] == "test":
        t_idx = int(sec["id"].split("_")[1])
        for set_data in sec["practice_sets"]:
            q_idx = set_data["set_index"]
            # Track 3 is Q1, Track 4 is Q2, etc.
            track_num = q_idx + 2
            set_data["audio"] = f"E26-T{t_idx:02d}-{track_num:02d}.mp3"

with open("data/part01_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("data/part01_data.js", "w", encoding="utf-8") as f:
    f.write("window.part01Data = ")
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write(";\n")

print("Fixed Test Audio in JSON/JS")
