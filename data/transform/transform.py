#!/usr/bin/env python3

import csv
import re
import sys
from pathlib import Path

def is_valid_email(email: str) -> bool:
    return bool(re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email))

PASSWORD = "2v4nddvG@!6sdlk8$3223cyfg$skldit"
COUNTRY = "United States"

# --- Company normalization ---
COMPANY_MAP = {
    "Catholic Charities of Northeast Kansas": "Catholic Charities",
    "Latinx Education Collaborative (EducaTec)": "LEC",
}

def normalize_company(name: str) -> str:
    if not name:
        return ""
    return COMPANY_MAP.get(name.strip(), name.strip())

# --- Language mapping for format 1 ---
def map_language(langsrc: str):
    if not langsrc:
        return "en", "EnglishSpeakers"
    langsrc = langsrc.lower()
    if "espanol" in langsrc or "spanish" in langsrc:
        return "es", "SpanishSpeakers"
    return "en", "EnglishSpeakers"

# --- Output headers ---
OUTPUT1_HEADER = [
    "First Name",
    "Last Name",
    "Username",
    "Email",
    "Force password reset at login (yes/no)",
    "Country",
    "Language (en/es/pt/fr)",
    "Groups (Separated with slashes)",
    "Companies (Separated with slashes)",
    "Address",
    "Phone",
    "Mobile",
    "Email Alternative",
    "Fax",
    "Office Phone",
    "Other Phone",
    "City",
    "Localization",
    "Manager (Username|ID)",
    "Department",
    "Position",
    "Employee Number",
    "Document",
    "Birthday",
    "Locations (Separated with slashes)",
]

OUTPUT2_HEADER = [
    "Full Name*",
    "Email*",
    "Phone",
    "Mobile",
    "Address",
    "Date of Birth",
    "Position",
    "Employee ID",
    "Company",
    "Department",
    "Manager"
]

# --- Load existing records for deduplication ---
# Builds a set of (firstname, lastname, phone) tuples for composite matching.
def load_existing_records(existing_file):
    records = set()
    if not existing_file or not Path(existing_file).is_file():
        return records

    with open(existing_file, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames or []

        # Detect file format based on available columns
        has_split_names = any(f in fieldnames for f in ("Last names", "Last Name", "lastname"))
        has_full_name   = "Full Name*" in fieldnames

        # Detect phone column (prefer mobile variants)
        phone_col = None
        for candidate in ("Phone", "Mobile", "mobile", "Phone (Mobile)", "phone"):
            if candidate in fieldnames:
                phone_col = candidate
                break

        for row in reader:
            phone = "".join(filter(str.isdigit, (row.get(phone_col) or "") if phone_col else ""))

            if has_split_names:
                if "Last names" in fieldnames:
                    ln = (row.get("Last names") or "").strip()
                elif "Last Name" in fieldnames:
                    ln = (row.get("Last Name") or "").strip()
                else:
                    ln = (row.get("lastname") or "").strip()

                # Try common first-name column names
                fn = ""
                for fn_col in ("Names", "First Name", "First names", "firstname", "name"):
                    if fn_col in fieldnames:
                        fn = (row.get(fn_col) or "").strip()
                        break

            elif has_full_name:
                parts = (row.get("Full Name*") or "").strip().split()
                fn = parts[0] if len(parts) >= 2 else ""
                ln = parts[-1] if parts else ""

            else:
                continue

            if not ln:
                continue

            key = (fn.lower(), ln.lower(), phone)
            records.add(key)

    print(f"Loaded {len(records)} existing record(s) from '{existing_file}' using phone col: '{phone_col}'")
    phone_present = sum(1 for (fn, ln, ph) in records if ph)
    print(f"  {phone_present} record(s) have a phone number; {len(records) - phone_present} do not (will match on name only)")
    return records

# --- Write Format 1 ---
def write_format1(row, writer, existing_records, skipped_names):
    firstname = (row.get("name") or "").strip()
    lastname  = (row.get("lastname") or "").strip()
    if not lastname:
        return
    phone_raw = (row.get("mobile") or "").strip()
    phone_digits = "".join(filter(str.isdigit, phone_raw))
    key_full      = (firstname.lower(), lastname.lower(), phone_digits)
    key_name_only = (firstname.lower(), lastname.lower(), "")
    if key_full in existing_records or key_name_only in existing_records:
        skipped_names.add((firstname, lastname, phone_raw))
        return

    email = (row.get("email") or "").strip()
    if not email or not is_valid_email(email):
        email = f"{firstname.replace(' ','').lower()}{lastname.replace(' ','').lower()}@unknownemail.io"

    phone     = phone_raw
    address   = (row.get("address") or "").strip()
    company   = normalize_company(row.get("company_name") or "")
    langsrc   = (row.get("language") or "").strip()

    lang, group = map_language(langsrc)

    writer.writerow([
        firstname,
        lastname,
        email,
        email,
        "no",
        COUNTRY,
        lang,
        group,
        company,
        address,
        phone,
        "", "", "", "", "", "", "", "", "", "", "", "", "",
        company
    ])

# --- Write Format 2 ---
def write_format2(row, writer, existing_records, skipped_names):
    firstname = (row.get("name") or "").strip()
    lastname  = (row.get("lastname") or "").strip()
    if not lastname:
        return
    phone_raw = (row.get("mobile") or "").strip()
    phone_digits = "".join(filter(str.isdigit, phone_raw))
    key_full      = (firstname.lower(), lastname.lower(), phone_digits)
    key_name_only = (firstname.lower(), lastname.lower(), "")
    if key_full in existing_records or key_name_only in existing_records:
        skipped_names.add((firstname, lastname, phone_raw))
        return

    email = (row.get("email") or "").strip()
    if not email or not is_valid_email(email):
        email = f"{firstname.replace(' ','').lower()}{lastname.replace(' ','').lower()}@unknownemail.io"

    phone      = phone_raw
    address    = (row.get("address") or "").strip()
    dob       = (row.get("birthday") or "").strip()
    position  = (row.get("position") or "").strip()
    emp_id    = (row.get("employee_number") or "").strip()
    company   = normalize_company(row.get("company_name") or "")
    department = (row.get("department") or "").strip()
    manager    = (row.get("manager_id") or "").strip()

    full_name = f"{firstname} {lastname}".strip()

    writer.writerow([
        full_name,
        email,
        phone,
        "",           # Mobile empty
        address,
        dob,
        position,
        emp_id,
        company,
        department,
        manager
    ])

# --- Main ---
def main(source_file, out1_file, out2_file, existing_file=None, log_file="skipped_duplicates.log"):
    existing_records = load_existing_records(existing_file)
    skipped_names = set()

    with open(source_file, newline='', encoding="utf-8-sig") as infile:
        reader = list(csv.DictReader(infile))

    # Debug: print sample keys from both sides for comparison
    print("\n--- Sample keys from EXISTING file (first 5) ---")
    for key in list(existing_records)[:5]:
        print(f"  fn={repr(key[0])}  ln={repr(key[1])}  phone={repr(key[2])}")

    print("\n--- Sample keys from SOURCE file (first 5) ---")
    for row in reader[:5]:
        fn = (row.get("name") or "").strip().lower()
        ln = (row.get("lastname") or "").strip().lower()
        phone = "".join(filter(str.isdigit, (row.get("mobile") or "").strip()))
        print(f"  fn={repr(fn)}  ln={repr(ln)}  phone={repr(phone)}")
    print("")

    with open(source_file, newline='', encoding="utf-8-sig") as infile:
        reader = list(csv.DictReader(infile))

    # Format 1
    if out1_file:
        with open(out1_file, "w", newline='', encoding="utf-8") as f1:
            writer1 = csv.writer(f1, quoting=csv.QUOTE_MINIMAL)
            writer1.writerow(OUTPUT1_HEADER)
            for row in reader:
                write_format1(row, writer1, existing_records, skipped_names)

    # Format 2
    if out2_file:
        with open(out2_file, "w", newline='', encoding="utf-8") as f2:
            writer2 = csv.writer(f2, quoting=csv.QUOTE_MINIMAL)
            writer2.writerow(OUTPUT2_HEADER)
            for row in reader:
                write_format2(row, writer2, existing_records, skipped_names)

    # Write log file
    if skipped_names:
        with open(log_file, "w", encoding="utf-8") as logf:
            logf.write("Skipped records (already exist in destination — matched on first name, last name, and phone):\n")
            logf.write(f"{'First Name':<20} {'Last Name':<20} {'Phone'}\n")
            logf.write("-" * 60 + "\n")
            for (fn, ln, phone) in sorted(skipped_names, key=lambda x: (x[1], x[0])):
                logf.write(f"{fn:<20} {ln:<20} {phone}\n")
        print(f"{len(skipped_names)} duplicate(s) skipped. See log file: {log_file}")

# --- Command-line ---
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: transform_combined.py source.csv format1.csv format2.csv existing.csv")
        print("Use empty string '' for a format you do not want to generate.")
        sys.exit(1)

    source_csv = sys.argv[1]
    format1_csv = sys.argv[2] if sys.argv[2] != '' else None
    format2_csv = sys.argv[3] if sys.argv[3] != '' else None
    existing_csv = sys.argv[4] if len(sys.argv) > 4 else None

    main(source_csv, format1_csv, format2_csv, existing_csv)
