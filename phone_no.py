import csv

# === File paths ===
matched_csv_path = "C:/Users/surya/OneDrive/Documents/Vscode/matched_resumes.csv"
master_csv_path = "C:/Users/surya/OneDrive/Documents/Vscode/raw_master_leads_duplicated.csv"
output_csv_path = "C:/Users/surya/OneDrive/Documents/Vscode/matched_resumes_filled.csv"

# === Step 1: Load email → Mobile or Phone (prioritize Mobile) ===
email_to_phone = {}

with open(master_csv_path, newline='', encoding='utf-8') as master_file:
    reader = csv.DictReader(master_file)
    for row in reader:
        email = row.get("Email", "").strip().lower()
        mobile = row.get("Mobile", "").strip()
        phone = row.get("Phone", "").strip()
        
        if email:
            if mobile:
                email_to_phone[email] = mobile
            elif phone:
                email_to_phone[email] = phone

# === Step 2: Fill missing phones in matched_resumes.csv ===
with open(matched_csv_path, newline='', encoding='utf-8') as matched_file, \
     open(output_csv_path, mode='w', newline='', encoding='utf-8') as out_file:

    reader = csv.DictReader(matched_file)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(out_file, fieldnames=fieldnames)
    writer.writeheader()

    filled_count = 0
    total_count = 0

    for row in reader:
        total_count += 1
        phone = row.get("Phone", "").strip()
        email = row.get("Email", "").strip().lower()

        if not phone and email in email_to_phone:
            row["Phone"] = email_to_phone[email]
            filled_count += 1

        writer.writerow(row)

print("✅ Completed filling missing phone numbers.")
print(f"🔢 Total records checked: {total_count}")
print(f"📞 Phone numbers filled: {filled_count}")
print(f"📁 Output saved to: {output_csv_path}")
