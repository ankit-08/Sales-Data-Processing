import os
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(BASE_DIR, "src", "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

SUMMARY_FILE = os.path.join(REPORT_DIR, "summary.csv")
PRODUCT_FILE = os.path.join(REPORT_DIR, "by_product.csv")
DATE_FILE = os.path.join(REPORT_DIR, "by_date.csv")

def _init_file(path, header):
    """
    Create file with header if:
    - file does not exist OR
    - file exists but is empty
    """
    if (not os.path.exists(path)) or os.path.getsize(path) == 0:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)

def write_reports(run_id, stats):
    # -------------------------
    # Ensure files + headers
    # -------------------------
    _init_file(
        SUMMARY_FILE,
        ["run_id", "files", "rows", "valid", "invalid", "total_quantity", "total_revenue"]
    )

    _init_file(
        PRODUCT_FILE,
        ["run_id", "product", "total_quantity", "total_revenue"]
    )

    _init_file(
        DATE_FILE,
        ["run_id", "date", "total_quantity", "total_revenue"]
    )

    # -------------------------
    # Summary report
    # -------------------------
    with open(SUMMARY_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            run_id,
            stats["files"],
            stats["rows"],
            stats["valid"],
            stats["invalid"],
            stats["quantity"],
            stats["revenue"]
        ])

    # -------------------------
    # By product report
    # -------------------------
    with open(PRODUCT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for product, values in stats["by_product"].items():
            writer.writerow([
                run_id,
                product,
                values["qty"],
                values["rev"]
            ])

    # -------------------------
    # By date report
    # -------------------------
    with open(DATE_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for date, values in stats["by_date"].items():
            writer.writerow([
                run_id,
                date,
                values["qty"],
                values["rev"]
            ])
