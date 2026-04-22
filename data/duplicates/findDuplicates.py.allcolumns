#!/usr/bin/env python3
"""
find_duplicates.py — Show all duplicate rows in a CSV file.

Usage:
    python find_duplicates.py <file.csv> [options]

Options:
    --columns COL1,COL2   Check duplicates on specific columns only (default: all)
    --keep-index          Show original row numbers (1-based, excluding header)
    --output <file.csv>   Save duplicate rows to a CSV file
"""

import csv
import sys
import argparse
from collections import defaultdict


def find_duplicates(filepath, columns=None, keep_index=False, output=None):
    with open(filepath, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)
        fieldnames = reader.fieldnames

    if not all_rows:
        print("The CSV file is empty.")
        return

    # Determine which columns to use for duplicate detection
    check_cols = columns if columns else fieldnames
    missing = [c for c in check_cols if c not in fieldnames]
    if missing:
        print(f"Error: Column(s) not found in CSV: {', '.join(missing)}")
        print(f"Available columns: {', '.join(fieldnames)}")
        sys.exit(1)

    # Group row indices by their key (tuple of values in check_cols)
    groups = defaultdict(list)
    for i, row in enumerate(all_rows):
        key = tuple(row[c] for c in check_cols)
        groups[key].append(i)

    # Keep only groups with more than one occurrence
    duplicate_groups = {k: v for k, v in groups.items() if len(v) > 1}

    if not duplicate_groups:
        print("No duplicate rows found.")
        return

    # Collect all duplicate rows in their original order
    dup_indices = sorted(i for indices in duplicate_groups.values() for i in indices)
    dup_rows = [(i, all_rows[i]) for i in dup_indices]

    total_dupes = len(dup_indices)
    unique_dupes = len(duplicate_groups)

    print(f"Found {total_dupes} duplicate rows ({unique_dupes} unique duplicated value set(s)).\n")

    if columns:
        print(f"Checked columns : {', '.join(check_cols)}")
        print(f"All columns     : {', '.join(fieldnames)}\n")

    # Print results as an aligned table
    display_fields = (["row"] if keep_index else []) + list(fieldnames)
    col_widths = {col: len(col) for col in display_fields}
    for i, row in dup_rows:
        if keep_index:
            col_widths["row"] = max(col_widths["row"], len(str(i + 1)))
        for col in fieldnames:
            col_widths[col] = max(col_widths[col], len(str(row.get(col, ""))))

    def fmt_row(values):
        return "  ".join(str(v).ljust(col_widths[col]) for col, v in zip(display_fields, values))

    header_vals = display_fields
    print(fmt_row(header_vals))
    print(fmt_row(["-" * col_widths[col] for col in display_fields]))

    for i, row in dup_rows:
        vals = []
        if keep_index:
            vals.append(i + 1)          # 1-based row number (excluding header)
        vals += [row.get(col, "") for col in fieldnames]
        print(fmt_row(vals))

    # Optionally save to file
    if output:
        with open(output, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for _, row in dup_rows:
                writer.writerow(row)
        print(f"\nDuplicate rows saved to: {output}")


def main():
    parser = argparse.ArgumentParser(description="Show duplicate rows in a CSV file.")
    parser.add_argument("file", help="Path to the CSV file")
    parser.add_argument(
        "--columns",
        help="Comma-separated list of columns to check (default: all)",
        default=None,
    )
    parser.add_argument(
        "--keep-index",
        action="store_true",
        help="Show original row numbers",
    )
    parser.add_argument(
        "--output",
        help="Save duplicate rows to this CSV file",
        default=None,
    )
    args = parser.parse_args()

    columns = [c.strip() for c in args.columns.split(",")] if args.columns else None

    find_duplicates(
        filepath=args.file,
        columns=columns,
        keep_index=args.keep_index,
        output=args.output,
    )


if __name__ == "__main__":
    main()
