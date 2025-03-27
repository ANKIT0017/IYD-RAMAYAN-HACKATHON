import json
import os
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

# Load Models
ankur = OllamaLLM(model="llama3.2:latest")  # Generates False and None inputs
aaditya = OllamaLLM(model="llama3.2:latest")  # Verifies if the statement is True/False/None

# Define the prompt template for generating false or irrelevant inputs
false_template = """
Forget previous conversations. You are tasked with generating an incorrect or irrelevant input based on the Valmiki Ramayana.
Your statement should sound plausible, feel like it was written by Valmiki, but must be historically inaccurate or irrelevant to the Ramayana. You will not generate any thing else . Do just as directed.

Original input:
{shloka_text}

Generated (False/None) Input:
"""

# Define the prompt template for classification
verify_template = """
Forget previous conversations and dont think. You will not generate any thing else . Do just as directed.. You will classify the given statement about the Valmiki Ramayana.
If the statement is factually correct, reply with "True".
If the statement is incorrect, reply with "False".
If the statement is irrelevant or not about Ramayana, reply with "None".

Statement: {shloka}

Answer:
"""

# Load input dataset containing real statements (now with "instruction", "input", and "output")
def load_real_shloka_data(filename=r"ankit\3aranya_kanda_NullRemoved.py"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    print("⚠️ Warning: No input dataset found.")
    return []

# Load existing dataset of generated false/none inputs
def load_existing_false_data(filename="false_none_dataset.json"):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # print("⚠️ Warning: JSON file is corrupted. Starting fresh.")
            return []
    return []

# Generate & Verify False/None Inputs
def generate_false_none_data():
    real_shlokas = load_real_shloka_data()
    false_none_dataset = load_existing_false_data()

    for entry in real_shlokas:
        original_input = entry.get("input", "").strip()

        if not original_input:
            continue  # Skip empty entries

        # Step 1: Generate a false/none input
        try:
            false_none_input = ankur.invoke(false_template.format(shloka_text=original_input)).strip()
            # print(f"Generated False/None Input: {false_none_input}")
        except Exception as e:
            print(f"Error generating false/none input: {e}")
            continue  # Skip if there was an error

        # Step 2: Verify the generated input
        try:
            verification_result = aaditya.invoke(verify_template.format(shloka=false_none_input)).strip()
            print(f"------  Verification Result: {verification_result}")
        except Exception as e:
            print(f"Error verifying input: {e}")
            continue  # Skip if there was an error

        # Step 3: Store only if False or None
        if verification_result in ["False", "None"]:
            false_none_dataset.append({
                "instruction": entry.get("instruction", ""),
                "input": false_none_input,
                "output": verification_result
            })

        # Save after each generation to prevent data loss
        save_dataset(false_none_dataset)

# Save dataset to JSON file
def save_dataset(dataset, filename=r"ankit\3aranya_kanda_false_none_dataset.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)
    # print(f"✅ False/None dataset saved as {filename}")

# Run the data generation
if __name__ == "__main__":
    generate_false_none_data()
    print("Process Completed.")
