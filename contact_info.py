import csv

# Input and output file paths
input_file = "C:/Users/surya/OneDrive/Documents/Vscode/leads_with_attachments.csv"
output_file = "C:/Users/surya/OneDrive/Documents/Vscode/leads_contact_info.csv"

# Fields to extract
selected_fields = ["FirstName", "LastName", "Phone", "Email", "AttachmentURLs"]

with open(input_file, newline='', encoding='utf-8') as infile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=selected_fields)
    writer.writeheader()

    count = 0
    for row in reader:
        filtered_row = {field: row.get(field, "").strip() for field in selected_fields}
        writer.writerow(filtered_row)
        count += 1

print(f"\n✅ Contact info extracted from leads_with_attachments.csv")
print(f"📁 Output saved to: {output_file}")
print(f"🔢 Total records: {count}")
