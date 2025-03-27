import json
import os
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

# Load Model (for generating False/None statements)
ankur = OllamaLLM(model="llama3.2:latest")

# Prompt template for generating False/None statements
false_none_template = """
Forget previous conversations. You are tasked with generating an incorrect or irrelevant statement based on the explanation and comments of a Valmiki Ramayana verse.
- The statement must sound plausible and feel like it was written by Valmiki but it is factually incorrect, classify it as "False".
- If the statement is irrelevant and not about Valmiki Ramayana, classify it as "None".

Explanation:
{explanation}

Comments:
{comments}

Generated Statement (Label it with False or None at the end):
"""



# Load input dataset containing real shlokas
# -----------------> {{{ Change file name here only }}}

def load_real_shloka_data(filename="3_Aranya_Kanda_NullRemoved.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    print("⚠️ Warning: No input dataset found.")
    return []

# Generate False/None statements
def generate_false_none_data():
    real_shlokas = load_real_shloka_data()
    false_none_dataset = []

    for entry in real_shlokas:
        explanation = entry.get("explanation", "").strip()
        comments = entry.get("comments", "").strip()

        if not explanation or not comments:
            continue  # Skip if missing explanation or comments

        try:
            generated_output = ankur.invoke(
                false_none_template.format(explanation=explanation, comments=comments)
            ).strip()

            # Extract classification (last word should be "False" or "None")
            if generated_output.endswith("False"):
                classification = "False"
                generated_statement = generated_output.replace("False", "").strip()
            elif generated_output.endswith("None"):
                classification = "None"
                generated_statement = generated_output.replace("None", "").strip()
            else:
                continue  # Skip if the response format is incorrect

            false_none_dataset.append({
                "index": f"{entry['sarga']}.{entry['shloka']}.{entry['kanda']}",  # Format: Sarga.Shloka.Kanda
                "original_shloka": entry["shloka_text"],
                "original_explanation": explanation,
                "original_comments": comments,
                "output": generated_statement,  # False/None statement
                "classification": classification  # Classification: False or None
            })

        except Exception as e:
            print(f"Error generating statement: {e}")
            continue  # Skip if error occurs

        save_dataset(false_none_dataset)

# Save dataset to Python file
def save_dataset(dataset, filename="1bala_kanda_false_none_STEP2.py"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

# Run the process
if __name__ == "__main__":
    generate_false_none_data()
    print("✅ Step 2 Completed: False/None statements generated.")
