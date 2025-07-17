import os
import csv
import shutil
import re

# Paths
csv_path = "C:/Users/surya/OneDrive/Documents/Vscode/leads_contact_info.csv"
files_folder = "C:/Users/surya/OneDrive/Documents/Vscode/Master_Resumes"
matched_folder = os.path.join(files_folder, "matched")
unmatched_folder = os.path.join(files_folder, "unmatched")
matched_log = os.path.join(files_folder, "matched_resumes.csv")
unmatched_log = os.path.join(files_folder, "unmatched_resumes.csv")

os.makedirs(matched_folder, exist_ok=True)
os.makedirs(unmatched_folder, exist_ok=True)

# Step 1: Load CSV into a dict with transformed email as key
email_data_map = {}

with open(csv_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        email = row.get("Email", "").strip().lower()
        if email:
            pattern = email.replace("@", "_").replace(".", "_")
            email_data_map[pattern] = {
                "FirstName": row.get("FirstName", "").strip(),
                "MiddleName": row.get("MiddleName", "").strip(),
                "LastName": row.get("LastName", "").strip(),
                "Phone": row.get("Phone", "").strip(),
                "Email": email,
                "AttachmentURLs": row.get("AttachmentURLs", "").strip()
            }

# Regex to remove trailing numbers like _6003345532
numeric_suffix = re.compile(r"^(.*)_\d{6,}$")

# Prepare log files
fieldnames = ["FirstName", "MiddleName", "LastName", "Phone", "Email", "AttachmentURLs", "Filename"]

with open(matched_log, mode='w', newline='', encoding='utf-8') as matched_file, \
     open(unmatched_log, mode='w', newline='', encoding='utf-8') as unmatched_file:

    matched_writer = csv.DictWriter(matched_file, fieldnames=fieldnames)
    unmatched_writer = csv.DictWriter(unmatched_file, fieldnames=fieldnames)

    matched_writer.writeheader()
    unmatched_writer.writeheader()

    matched_count = 0
    unmatched_count = 0
    matched_keys = set()

    for filename in os.listdir(files_folder):
        if not filename.lower().endswith((".pdf", ".docx", ".doc")):
            continue

        filepath = os.path.join(files_folder, filename)
        name_part = os.path.splitext(filename)[0].lower()

        # Remove trailing _digits
        match = numeric_suffix.match(name_part)
        base_key = match.group(1) if match else name_part

        if base_key in email_data_map:
            shutil.move(filepath, os.path.join(matched_folder, filename))
            data = email_data_map[base_key]
            data["Filename"] = filename
            matched_writer.writerow(data)
            matched_keys.add(base_key)
            matched_count += 1
        else:
            shutil.move(filepath, os.path.join(unmatched_folder, filename))
            unmatched_writer.writerow({
                "FirstName": "", "MiddleName": "", "LastName": "", "Phone": "",
                "Email": "", "AttachmentURLs": "", "Filename": filename
            })
            unmatched_count += 1

    # Optionally: record CSV entries that had no matching file
    for key, data in email_data_map.items():
        if key not in matched_keys:
            data["Filename"] = ""
            unmatched_writer.writerow(data)
            unmatched_count += 1

# Final report
print("\n✅ File classification and logging complete.")
print(f"📁 Matched files: {matched_count} → {matched_log}")
print(f"📁 Unmatched records (files or entries): {unmatched_count} → {unmatched_log}")
print(f"📂 Files moved to: {matched_folder} and {unmatched_folder}")
