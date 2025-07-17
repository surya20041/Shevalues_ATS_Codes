import csv

# Input and output paths
input_file = "C:/Users/surya/OneDrive/Documents/Vscode/master_leads.csv"
with_attachments_file = "C:/Users/surya/OneDrive/Documents/Vscode/leads_with_attachments.csv"
without_attachments_file = "C:/Users/surya/OneDrive/Documents/Vscode/leads_without_attachments.csv"

# Counters
count_with = 0
count_without = 0

with open(input_file, newline='', encoding='utf-8') as infile, \
     open(with_attachments_file, mode='w', newline='', encoding='utf-8') as with_file, \
     open(without_attachments_file, mode='w', newline='', encoding='utf-8') as without_file:

    reader = csv.DictReader(infile)
    headers = reader.fieldnames

    writer_with = csv.DictWriter(with_file, fieldnames=headers)
    writer_without = csv.DictWriter(without_file, fieldnames=headers)

    writer_with.writeheader()
    writer_without.writeheader()

    for row in reader:
        url = row.get("AttachmentURLs", "").strip()
        if url:
            writer_with.writerow(row)
            count_with += 1
        else:
            writer_without.writerow(row)
            count_without += 1

print(f"\n✅ Split complete.")
print(f"📁 Records with attachments: {count_with} → {with_attachments_file}")
print(f"📁 Records without attachments: {count_without} → {without_attachments_file}")
