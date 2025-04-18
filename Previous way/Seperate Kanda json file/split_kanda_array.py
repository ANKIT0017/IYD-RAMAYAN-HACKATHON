import json

# Load input JSON file
with open("Valmiki_Ramayan_Shlokas.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Dictionary to store kanda-wise data
kanda_dict = {}

# Categorize shlokas by kanda
for entry in data:
    kanda_name = entry["kanda"]
    if kanda_name not in kanda_dict:
        kanda_dict[kanda_name] = []
    kanda_dict[kanda_name].append(entry)

# Write separate JSON files for each kanda
for index, (kanda, shlokas) in enumerate(kanda_dict.items(), start=1):
    file_name = f"diffrent py file of Kanda\{index}_{kanda.replace(' ', '_')}.json"
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(shlokas, file, ensure_ascii=False, indent=4)
    print(f"File created: {file_name}")