import json

# Load input JSON file
with open("Valmiki_Ramayan_Shlokas.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Dictionary to store kanda-wise data
kanda_dict = {}

# Categorize shlokas by kanda, filtering out entries with null explanation
for entry in data:
    if not entry.get("explanation"):  # Skip if explanation is null or empty
        continue
    
    # Replace null comments with empty string " . "
    if entry.get("comments") is None:
        entry["comments"] = " . "
    
    kanda_name = entry["kanda"]
    if kanda_name not in kanda_dict:
        kanda_dict[kanda_name] = []
    kanda_dict[kanda_name].append(entry)

# Write separate JSON files for each kanda
for index, (kanda, shlokas) in enumerate(kanda_dict.items(), start=1):
    file_name = f"Seperate Kanda NullRemoved json file\{index}_{kanda.replace(' ', '_')}_NullRemoved.json"
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(shlokas, file, ensure_ascii=False, indent=4)
    print(f"File created: {file_name}")
