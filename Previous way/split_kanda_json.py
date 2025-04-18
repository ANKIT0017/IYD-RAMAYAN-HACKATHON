import json
from collections import defaultdict

# Load the input JSON file
with open("Valmiki_Ramayan_Shlokas.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Group shlokas by Kanda
kanda_dict = defaultdict(list)
for shloka in data:
    kanda = shloka["kanda"]
    output_entry = {
        "instruction": "Determine if the following shloka belongs to the Valmiki Ramayana.",
        "input": shloka["explanation"],
        "output": f"true, this is from {shloka['kanda']}, Sarga {shloka['sarga']} of Valmiki Ramayana."
    }
    kanda_dict[kanda].append(output_entry)

# Save each Kanda's data into separate JSON files
for kanda, shlokas in kanda_dict.items():
    filename = f"{kanda.replace(' ', '_').lower()}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(shlokas, f, ensure_ascii=False, indent=2)
    print(f"Saved: {filename}")