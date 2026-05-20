"""
CSV Conversion Script
Converts source CSV format to destination CSV format.

Field Mapping:
  Source "First Name"           -> Destination "name"
  Source "Last Name"            -> Destination "lastname"
  Source "Email"                -> Destination "email"
  Source "Cell Phone"           -> Destination "mobile"
  Source "Address"              -> Destination "address"
  Source "Distribution Partner" -> Destination "company_name"
  Source "Preferred Language"   -> Destination "language"

All other source fields are discarded.
All other destination fields are included as empty columns.
"""

import csv
import sys
import os

# Mapping: source column name -> destination column name
FIELD_MAPPING = {
    "First Name":             "name",
    "Last Name":              "lastname",
    "Email":                  "email",
    "Cell Phone":             "mobile",
    "Address":                "address",
    "Distribution Partner":   "company_name",
    "Preferred Language":     "language",
}

# All destination columns in order (unmapped fields will be written as empty)
DEST_FIELDS = [
    "username", "employee_number", "country", "lastname", "user_type", "department",
    "mobile", "city", "name", "id", "other_email", "is_deleted", "other", "email",
    "doc", "birthday", "office", "position", "phone", "is_disabled", "location",
    "is_external", "role_name", "type", "address", "fax", "manager_id", "company_name",
    "language",
]


def convert(input_path: str, output_path: str) -> None:
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(1)

    with open(input_path, newline="", encoding="utf-8-sig") as infile, \
         open(output_path, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=DEST_FIELDS)
        writer.writeheader()

        missing = [src for src in FIELD_MAPPING if src not in reader.fieldnames]
        if missing:
            print(f"Warning: These expected source columns were not found and will be blank: {missing}")

        rows_written = 0
        for row in reader:
            dest_row = {dest: "" for dest in DEST_FIELDS}
            for src, dest in FIELD_MAPPING.items():
                dest_row[dest] = row.get(src, "").strip()
            writer.writerow(dest_row)
            rows_written += 1

    print(f"Done! {rows_written} rows written to '{output_path}'.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_csv.py <input_file.csv> <output_file.csv>")
        print("Example: python convert_csv.py source.csv destination.csv")
        sys.exit(1)

    convert(sys.argv[1], sys.argv[2])
