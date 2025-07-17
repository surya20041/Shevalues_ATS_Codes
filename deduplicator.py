import os
import csv

# Input & output paths
csv_folder = "C:/Users/surya/OneDrive/Documents/Vscode/converted_csvs"
output_master = "C:/Users/surya/OneDrive/Documents/Vscode/master_leads.csv"
output_duplicates = "C:/Users/surya/OneDrive/Documents/Vscode/duplicates_leads.csv"

# Get all Leads_*.csv files
csv_files = [
    os.path.join(csv_folder, f)
    for f in os.listdir(csv_folder)
    if f.lower().startswith("leads") and f.lower().endswith(".csv")
]

if not csv_files:
    print("❌ No Leads_*.csv files found.")
    exit()

# Get headers from the first file
with open(csv_files[0], newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames

seen_name_keys = set()
total_rows = 0
unique_rows = 0
duplicate_rows = 0

# Open both output files
with open(output_master, mode='w', newline='', encoding='utf-8') as master_file, \
     open(output_duplicates, mode='w', newline='', encoding='utf-8') as dup_file:

    master_writer = csv.DictWriter(master_file, fieldnames=headers)
    dup_writer = csv.DictWriter(dup_file, fieldnames=headers)

    master_writer.writeheader()
    dup_writer.writeheader()

    for csv_file in csv_files:
        print(f"📄 Processing: {os.path.basename(csv_file)}")
        try:
            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    total_rows += 1

                    fname = row.get("FirstName", "").strip().lower()
                    mname = row.get("MiddleName", "").strip().lower()
                    lname = row.get("LastName", "").strip().lower()

                    if not fname and not lname:
                        print(f"⚠️ Skipped row with empty name in {csv_file}")
                        continue

                    name_key = (fname, mname, lname)

                    if name_key not in seen_name_keys:
                        seen_name_keys.add(name_key)
                        master_writer.writerow(row)
                        unique_rows += 1
                    else:
                        dup_writer.writerow(row)
                        duplicate_rows += 1

        except Exception as e:
            print(f"❌ Error processing {csv_file}: {e}")

# Summary
print("\n✅ Merge complete.")
print(f"🔢 Total rows scanned: {total_rows}")
print(f"✅ Unique rows written: {unique_rows} → {output_master}")
print(f"⚠️ Duplicate rows written: {duplicate_rows} → {output_duplicates}")
