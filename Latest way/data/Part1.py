import os                           #For file Naming
from bs4 import BeautifulSoup       #Helps in extraction of data from HTML
import csv                          #for output file

book_mapping = {
    "Book IV": "4Kishkindha",
    "Book III": "3Aranya",
    "Book II": "2Ayodhya",
    "Book I": "1Bala",
    "Book VII": "7Uttara",
    "Book VI": "6Yuddha",
    "Book V": "5Sundara",
}
# we set name of the book as <BookNumber><BookName>, so as to display the data in chronological manner, howser part2 will resolve this thing

all_data = []

# Traverse all folders and HTML files
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            input_file = os.path.join(root, file)
            print(f"🔍 Processing: {input_file}")

            with open(input_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            soup = BeautifulSoup(html_content, 'lxml')

            # --- Book Name Extraction --- from the title of the html file
            book_name = "Unknown"
            for h3 in soup.find_all('h3'):
                if not h3.text:
                    continue
                cleaned_text = ' '.join(h3.get_text().split())
                for key in book_mapping:
                    if key in cleaned_text:
                        book_name = book_mapping[key]
                        break
                if book_name != "Unknown":
                    break


            # --- Sarga Number Extraction --- from the heading, if not present then from the title
            
            sarga_number = "Unknown"
            sarga_h3 = soup.find('h3', string=lambda x: x and 'Chapter [Sarga]' in x)
            if sarga_h3:
                parts = sarga_h3.get_text().split()
                for part in parts:
                    if part.isdigit():
                        sarga_number = part
                        break
            if sarga_number == "Unknown" and soup.title:
                parts = soup.title.string.split()
                for part in parts:
                    if part.isdigit():
                        sarga_number = part
                        break

            # --- Extract Verses --- from the verse id of the 
            import re  # Add this at top of your file if not already

            processed_verses = set()
            for verse in soup.find_all('p', class_='SanSloka'):
                sanshlok_parts = []
                for elem in verse.descendants:
                    if elem.name == 'br':
                        sanshlok_parts.append('\n')
                    elif isinstance(elem, str):
                        sanshlok_parts.append(elem.strip())
                sanshlok = ' '.join(sanshlok_parts).strip()

                if not sanshlok:
                    continue

                translit = verse.find_next('p', class_='pratipada')
                transliteration = translit.get_text(strip=True) if translit else ''

                translation = verse.find_next('p', class_='tat')
                translation_text = translation.get_text(strip=True) if translation else ''

                comment = verse.find_next('p', class_='comment')
                comment_text = comment.get_text(strip=True) if comment else ''

                # 💡 Extract verse number from start of transliteration
                verse_number = ''
                if transliteration:
                    match = re.match(r'^([0-9]{1,3}[a-zA-Z]?(\s*,\s*[0-9]{1,3}[a-zA-Z]?)*)(\.|\:)?\s+', transliteration)
                    if match:
                        verse_number = match.group(1).replace(' ', '')  # remove spaces inside the match

                if not verse_number:
                    continue  # skip if no verse number found

                if verse_number in processed_verses:
                    continue
                processed_verses.add(verse_number)

                all_data.append([
                    book_name,
                    sarga_number,
                    verse_number,
                    sanshlok,
                    transliteration,
                    translation_text,
                    comment_text
                ])

output_file = 'Part1_Output_FullHTMLdata.csv'

with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Kanda/Book Name", "Sarga/Chapter Number", "Shlok/Verse Number", "Sanshlok", "Transliteration", "Translation", "Comment"])
    writer.writerows(all_data)
print(f"\n✅ Extracted {len(all_data)} total verses into '{output_file}'")
