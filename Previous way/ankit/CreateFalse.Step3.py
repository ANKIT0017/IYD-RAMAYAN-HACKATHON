import json
import os

# Load false/none statements dataset
def load_false_none_data(filename="1bala_kanda_false_none_STEP2.py"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    print("⚠️ Warning: No dataset found.")
    return []

# Process and save the final dataset
def filter_false_none_data():
    false_none_data = load_false_none_data()
    filtered_dataset = []

    for entry in false_none_data:
        filtered_dataset.append({
            "index": entry["index"],
            "original_shloka": entry["original_shloka"],
            "original_explanation": entry["original_explanation"],
            "original_comments": entry["original_comments"],
            "generated_statement": entry["output"],  # Keeping only generated text
            "classification": entry["classification"]  # Keeping classification
        })

    save_dataset(filtered_dataset)

# Save dataset to JSON file
def save_dataset(dataset, filename="1bala_kanda_Filtered_false_noneSTEP3.py"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

# Run the process
if __name__ == "__main__":
    filter_false_none_data()
    print("✅ Step 3 Completed: Filtered dataset saved.")
