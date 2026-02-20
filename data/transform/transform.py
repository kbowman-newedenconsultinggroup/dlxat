#!/usr/bin/env python3

import csv
import sys
from pathlib import Path

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
    "Password (If empty the user will receive an email to set their password)",
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

# --- Load lastnames from existing file for deduplication ---
def load_existing_lastnames(existing_file):
    lastnames = set()
    if not existing_file or not Path(existing_file).is_file():
        return lastnames

    with open(existing_file, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)

        # Choose column to extract lastname
        if "Last names" in reader.fieldnames:
            col = "Last names"
        elif "Last Name" in reader.fieldnames:
            col = "Last Name"
        elif "lastname" in reader.fieldnames:
            col = "lastname"
        elif "Full Name*" in reader.fieldnames:
            col = "Full Name*"
        else:
            return lastnames

        for row in reader:
            ln = (row.get(col) or "").strip()
            if not ln:
                continue
            if col == "Full Name*":
                ln = ln.split()[-1]  # last word as lastname
            lastnames.add(ln.lower())
    return lastnames

# --- Write Format 1 ---
def write_format1(row, writer, existing_lastnames, skipped_names):
    firstname = (row.get("name") or "").strip()
    lastname  = (row.get("lastname") or "").strip()
    if not lastname:
        return
    key = lastname.lower()
    if key in existing_lastnames:
        skipped_names.add(lastname)
        return

    email = (row.get("email") or "").strip()
    if not email:
        email = f"{lastname.replace(' ','').lower()}@unknown.com"

    phone     = (row.get("mobile") or "").strip()
    address   = (row.get("address") or "").strip()
    company   = normalize_company(row.get("company_name") or "")
    langsrc   = (row.get("language") or "").strip()

    lang, group = map_language(langsrc)

    writer.writerow([
        firstname,
        lastname,
        email,
        email,
        PASSWORD,
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
def write_format2(row, writer, existing_lastnames, skipped_names):
    firstname = (row.get("name") or "").strip()
    lastname  = (row.get("lastname") or "").strip()
    if not lastname:
        return
    key = lastname.lower()
    if key in existing_lastnames:
        skipped_names.add(lastname)
        return

    email = (row.get("email") or "").strip()
    if not email:
        email = f"{lastname.replace(' ','').lower()}@unknown.com"

    phone     = (row.get("mobile") or "").strip()
    address   = (row.get("address") or "").strip()
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
def main(source_file, out1_file, out2_file, existing_file=None, log_file="skipped_lastnames.log"):
    existing_lastnames = load_existing_lastnames(existing_file)
    skipped_names = set()

    with open(source_file, newline='', encoding="utf-8-sig") as infile:
        reader = list(csv.DictReader(infile))

    # Format 1
    if out1_file:
        with open(out1_file, "w", newline='', encoding="utf-8") as f1:
            writer1 = csv.writer(f1, quoting=csv.QUOTE_MINIMAL)
            writer1.writerow(OUTPUT1_HEADER)
            for row in reader:
                write_format1(row, writer1, existing_lastnames, skipped_names)

    # Format 2
    if out2_file:
        with open(out2_file, "w", newline='', encoding="utf-8") as f2:
            writer2 = csv.writer(f2, quoting=csv.QUOTE_MINIMAL)
            writer2.writerow(OUTPUT2_HEADER)
            for row in reader:
                write_format2(row, writer2, existing_lastnames, skipped_names)

    # Write log file
    if skipped_names:
        with open(log_file, "w", encoding="utf-8") as logf:
            logf.write("Skipped lastnames (already exist in existing CSV):\n")
            for name in sorted(skipped_names):
                logf.write(name + "\n")
        print(f"{len(skipped_names)} names skipped. See log file: {log_file}")

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
