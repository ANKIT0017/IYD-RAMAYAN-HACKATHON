import os
import csv
from bs4 import BeautifulSoup

# Root directory containing subfolders like aranya, baala, etc.
DATA_DIR = r"C:\Users\krish\Desktop\IYD_webscrapper\extracted verse from html\data"
OUTPUT_CSV = "ramayan_verses.csv"
MISSING_FILE_LOG = "missing_files.log"

def extract_from_html(file_path, book_name, sarga_number, writer):
    print(f"Processing: (Book: {book_name}, Sarga: {sarga_number})")
    
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    sloka_tags = soup.find_all("p", class_="SanSloka")
    pratipada_tags = soup.find_all("p", class_="pratipada")
    tat_tags = soup.find_all("p", class_="tat")

    verse_index = 1
    for i in range(len(sloka_tags)):
        sanskrit = sloka_tags[i].get_text(strip=True)

        transliteration = ""
        translation = ""

        if i < len(pratipada_tags):
            transliteration = pratipada_tags[i].get_text(strip=True)
        if i < len(tat_tags):
            translation = tat_tags[i].get_text(strip=True)

        writer.writerow([book_name, sarga_number, verse_index, sanskrit, transliteration, translation])
        verse_index += 1

def main():
    print("Starting extraction...\n")
    missing_files = []  # List to store missing file paths
    
    with open(OUTPUT_CSV, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Book Name", "Sarga", "Verse Number", "Sanskrit", "Transliteration", "Translation"])

        for root, dirs, files in os.walk(DATA_DIR):
            for filename in sorted(files):
                if filename.endswith(".html"):
                    file_path = os.path.join(root, filename)

                    base = os.path.basename(file_path)  # e.g., aranya_6.html
                    folder = os.path.basename(root)     # e.g., aranya

                    if "_" in base:
                        parts = base.split("_")
                        if len(parts) == 2 and parts[1].endswith(".html"):
                            sarga_number = parts[1].replace(".html", "")
                            
                            if os.path.exists(file_path):
                                extract_from_html(file_path, folder, sarga_number, writer)
                            else:
                                missing_files.append(file_path)  # Log missing file path
                                print(f"❌ File missing: {file_path}")

    # Log missing files
    if missing_files:
        with open(MISSING_FILE_LOG, mode='w', encoding='utf-8') as log_file:
            for missing_file in missing_files:
                log_file.write(f"{missing_file}\n")
        
        print(f"\n❌ Some files were missing. Please check the missing files log at {MISSING_FILE_LOG}")
    
    print("\n✅ Extraction complete! Output saved to:", OUTPUT_CSV)

if __name__ == "__main__":
    main()
