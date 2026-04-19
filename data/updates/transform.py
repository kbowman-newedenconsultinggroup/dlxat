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
# Builds a set of (firstname, lastname, phone) tuples for composite matching,
# and a dict mapping each key -> (dest_email, full_dest_row) for email comparison.
def load_existing_records(existing_file):
    records  = set()
    email_map = {}   # key -> (dest_email, dest_row_dict)

    if not existing_file or not Path(existing_file).is_file():
        return records, email_map

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

        # Detect email column
        email_col = None
        for candidate in ("Email", "email", "Email*", "Email Address"):
            if candidate in fieldnames:
                email_col = candidate
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

            if email_col:
                dest_email = (row.get(email_col) or "").strip()
                email_map[key] = (dest_email, dict(row))

    print(f"Loaded {len(records)} existing record(s) from '{existing_file}' using phone col: '{phone_col}'")
    phone_present = sum(1 for (fn, ln, ph) in records if ph)
    print(f"  {phone_present} record(s) have a phone number; {len(records) - phone_present} do not (will match on name only)")
    print(f"  {len(email_map)} record(s) have an email address available for comparison")
    return records, email_map

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

# --- Email mismatch detection ---
# Compares source emails against destination emails for matched records.
# Writes destination rows (Format 1 shape) to a CSV where emails differ.
def write_email_mismatches(source_rows, email_map, mismatch_file="email_mismatches.csv"):
    mismatches = []

    for row in source_rows:
        firstname    = (row.get("name") or "").strip()
        lastname     = (row.get("lastname") or "").strip()
        if not lastname:
            continue

        phone_raw    = (row.get("mobile") or "").strip()
        phone_digits = "".join(filter(str.isdigit, phone_raw))

        src_email = (row.get("email") or "").strip().lower()

        # Try full key first, then name-only fallback
        key_full      = (firstname.lower(), lastname.lower(), phone_digits)
        key_name_only = (firstname.lower(), lastname.lower(), "")

        matched_key = None
        if key_full in email_map:
            matched_key = key_full
        elif key_name_only in email_map:
            matched_key = key_name_only

        if matched_key is None:
            continue  # Not in destination at all — not a mismatch case

        dest_email, dest_row = email_map[matched_key]

        if not dest_email:
            continue  # Destination has no email to compare

        if src_email == dest_email.lower():
            continue  # Emails match — no issue

        # Emails differ: collect destination row data for output
        # Reconstruct a Format-1-compatible row from the destination record
        fn = firstname
        ln = lastname

        # Pull fields from dest_row using flexible column name detection
        def get(dest_row, *candidates):
            for c in candidates:
                v = dest_row.get(c)
                if v is not None:
                    return v.strip()
            return ""

        phone_out  = get(dest_row, "Phone", "Mobile", "mobile", "phone")
        address    = get(dest_row, "Address", "address")
        company    = normalize_company(get(dest_row, "Companies (Separated with slashes)",
                                           "Company", "company_name", "company"))
        lang_raw   = get(dest_row, "Language (en/es/pt/fr)", "language")
        lang, group = map_language(lang_raw)
        department = get(dest_row, "Department", "department")
        position   = get(dest_row, "Position", "position")
        emp_num    = get(dest_row, "Employee Number", "employee_number")
        birthday   = get(dest_row, "Birthday", "birthday", "Date of Birth")
        manager    = get(dest_row, "Manager (Username|ID)", "manager_id", "Manager")

        mismatches.append({
            "First Name":                          fn,
            "Last Name":                           ln,
            "Username":                            dest_email,
            "Email":                               dest_email,
            "Force password reset at login (yes/no)": "no",
            "Country":                             COUNTRY,
            "Language (en/es/pt/fr)":              lang,
            "Groups (Separated with slashes)":     group,
            "Companies (Separated with slashes)":  company,
            "Address":                             address,
            "Phone":                               phone_out,
            "Mobile":                              "",
            "Email Alternative":                   "",
            "Fax":                                 "",
            "Office Phone":                        "",
            "Other Phone":                         "",
            "City":                                "",
            "Localization":                        "",
            "Manager (Username|ID)":               manager,
            "Department":                          department,
            "Position":                            position,
            "Employee Number":                     emp_num,
            "Document":                            "",
            "Birthday":                            birthday,
            "Locations (Separated with slashes)":  company,
            # Extra columns for traceability
            "_source_email":                       src_email,
            "_dest_email":                         dest_email,
        })

    if not mismatches:
        print("No email mismatches found between source and destination.")
        return

    # Write mismatch CSV — Format 1 columns + two audit columns
    mismatch_header = OUTPUT1_HEADER + ["Source Email (incorrect)", "Destination Email (correct)"]
    with open(mismatch_file, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(mismatch_header)
        for m in mismatches:
            writer.writerow([
                m["First Name"],
                m["Last Name"],
                m["Username"],
                m["Email"],
                m["Force password reset at login (yes/no)"],
                m["Country"],
                m["Language (en/es/pt/fr)"],
                m["Groups (Separated with slashes)"],
                m["Companies (Separated with slashes)"],
                m["Address"],
                m["Phone"],
                m["Mobile"],
                m["Email Alternative"],
                m["Fax"],
                m["Office Phone"],
                m["Other Phone"],
                m["City"],
                m["Localization"],
                m["Manager (Username|ID)"],
                m["Department"],
                m["Position"],
                m["Employee Number"],
                m["Document"],
                m["Birthday"],
                m["Locations (Separated with slashes)"],
                m["_source_email"],
                m["_dest_email"],
            ])

    print(f"{len(mismatches)} email mismatch(es) found. Destination rows written to: {mismatch_file}")

# --- Main ---
def main(source_file, out1_file, out2_file, existing_file=None, log_file="skipped_duplicates.log"):
    existing_records, email_map = load_existing_records(existing_file)
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

    # Email mismatch report (uses destination rows with correct emails)
    print("\n--- Checking for email mismatches ---")
    write_email_mismatches(reader, email_map)

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
