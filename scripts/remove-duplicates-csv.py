import csv

def remove_duplicates(input_csv, output_csv):
    seen = set()  # Set to track unique rows based on specific fields
    unique_rows = []

    with open(input_csv, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        # Collect only unique rows based on 'Source', 'Arabic Text', and 'English Translation'
        for row in reader:
            # Create a tuple excluding 'YouTube Timestamp' for comparison
            row_tuple = (row['Source'], row['Arabic Text'], row['English Translation'])
            if row_tuple not in seen:
                seen.add(row_tuple)  # Add to set if unique
                unique_rows.append(row)  # Add to unique rows list

    # Write unique rows to a new CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(unique_rows)

    print(f"Duplicates removed based on Source, Arabic Text, and English Translation. Unique data saved to {output_csv}")

# Usage
remove_duplicates('quotes_output.csv', 'quotes_output_unique.csv')
