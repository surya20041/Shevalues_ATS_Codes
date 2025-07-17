import os
import csv
import shutil
import re

# Paths
contact_csv = "C:/Users/surya/OneDrive/Documents/Vscode/leads_deduplicated.csv"
raw_csv = "C:/Users/surya/OneDrive/Documents/Vscode/raw_master_leads_duplicated.csv"
files_folder = "C:/Users/surya/OneDrive/Documents/Vscode/Master_Resumes"
matched_folder = os.path.join(files_folder, "matched")
unmatched_folder = os.path.join(files_folder, "unmatched")
matched_log = os.path.join(files_folder, "matched_resumes.csv")
unmatched_log = os.path.join(files_folder, "unmatched_resumes.csv")

os.makedirs(matched_folder, exist_ok=True)
os.makedirs(unmatched_folder, exist_ok=True)

# Load data from leads_contact_info.csv for classification and matched log
match_map = {}
with open(contact_csv, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        email = row.get("Email", "").strip().lower()
        if email:
            key = email.replace("@", "_").replace(".", "_")
            match_map[key] = {
                "FirstName": row.get("FirstName", "").strip(),
                "MiddleName": row.get("MiddleName", "").strip(),
                "LastName": row.get("LastName", "").strip(),
                "Phone": row.get("Phone", "").strip(),
                "Email": email,
                "AttachmentURLs": row.get("AttachmentURLs", "").strip()
            }

# Load data from raw_master_leads_duplicated.csv for unmatched log filling only
fallback_map = {}
with open(raw_csv, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        email = row.get("Email", "").strip().lower()
        if email:
            key = email.replace("@", "_").replace(".", "_")
            fallback_map[key] = {
                "FirstName": row.get("FirstName", "").strip(),
                "MiddleName": row.get("MiddleName", "").strip(),
                "LastName": row.get("LastName", "").strip(),
                "Phone": row.get("Phone", "").strip(),
                "Email": email,
                "AttachmentURLs": row.get("AttachmentURLs", "").strip()
            }

# Regex to strip trailing numeric suffix
numeric_suffix = re.compile(r"^(.*)_\d{6,}$")

# Output fields
fieldnames = ["FirstName", "MiddleName", "LastName", "Phone", "Email", "AttachmentURLs", "Filename"]

# Write logs
with open(matched_log, mode='w', newline='', encoding='utf-8') as matched_file, \
     open(unmatched_log, mode='w', newline='', encoding='utf-8') as unmatched_file:

    matched_writer = csv.DictWriter(matched_file, fieldnames=fieldnames)
    unmatched_writer = csv.DictWriter(unmatched_file, fieldnames=fieldnames)

    matched_writer.writeheader()
    unmatched_writer.writeheader()

    matched_count = 0
    unmatched_count = 0

    for filename in os.listdir(files_folder):
        if not filename.lower().endswith((".pdf", ".docx", ".doc")):
            continue

        filepath = os.path.join(files_folder, filename)
        name_part = os.path.splitext(filename)[0].lower()

        match = numeric_suffix.match(name_part)
        base_key = match.group(1) if match else name_part

        row = {
            "FirstName": "", "MiddleName": "", "LastName": "",
            "Phone": "", "Email": "", "AttachmentURLs": "", "Filename": filename
        }

        if base_key in match_map:
            shutil.move(filepath, os.path.join(matched_folder, filename))
            row.update(match_map[base_key])
            matched_writer.writerow(row)
            matched_count += 1
        else:
            shutil.move(filepath, os.path.join(unmatched_folder, filename))
            if base_key in fallback_map:
                row.update(fallback_map[base_key])
            unmatched_writer.writerow(row)
            unmatched_count += 1

# Final report
print("\n✅ Classification and logging complete.")
print(f"📁 Matched resumes:   {matched_count} → {matched_log}")
print(f"📁 Unmatched resumes: {unmatched_count} → {unmatched_log}")
print(f"📂 Files moved to:    {matched_folder} and {unmatched_folder}")
