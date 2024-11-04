import xml.etree.ElementTree as ET
import csv

def extract_from_docbook(xml_file, csv_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    namespace = {'': 'http://docbook.org/ns/docbook'}

    data = []
    unique_entries = set()  # Set to track unique entries

    # Traverse each section with arguments
    for section in root.findall(".//section[@role='arguments']", namespace):
        # Traverse each argument section within arguments
        for sub_section in section.findall("section", namespace):
            # Extract source information
            source = sub_section.find(".//blockquote/attribution", namespace)
            arabic_text = sub_section.find(".//blockquote/attribution[citetitle='Arabic']/../simpara", namespace)
            english_text = sub_section.find(".//blockquote/attribution[citetitle='English']/../simpara", namespace)
            timestamp = sub_section.find(".//simpara[@role='timestamp']/link", namespace)

            if source is not None and arabic_text is not None and english_text is not None and timestamp is not None:
                entry_tuple = (source.text.strip(), arabic_text.text.strip(), english_text.text.strip(), timestamp.get('{http://www.w3.org/1999/xlink}href'))
                
                # Only add entry if it's unique
                if entry_tuple not in unique_entries:
                    unique_entries.add(entry_tuple)  # Add to set to track uniqueness
                    entry = {
                        "Source": entry_tuple[0],
                        "Arabic Text": entry_tuple[1],
                        "English Translation": entry_tuple[2],
                        "YouTube Timestamp": entry_tuple[3]
                    }
                    data.append(entry)
                    print(f"Unique entry added: {entry}")

    # Write to CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Source", "Arabic Text", "English Translation", "YouTube Timestamp"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)

    print(f"Data extracted and saved to {csv_file}")

# Usage
extract_from_docbook('source_quotes.xml', 'quotes_output.csv')
