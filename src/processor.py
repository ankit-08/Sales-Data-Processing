import os
import csv
import logging
from collections import defaultdict

from .validators import validate_row, normalize_row
from .reports import write_reports
from .context import RUN_ID

# ============================================================
# PATHS
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_IN = os.path.join(BASE_DIR, "data", "in")
DATA_OUT = os.path.join(BASE_DIR, "data", "out")
DATA_ERR = os.path.join(BASE_DIR, "data", "err")

os.makedirs(DATA_OUT, exist_ok=True)
os.makedirs(DATA_ERR, exist_ok=True)

ERROR_THRESHOLD = 5

# ============================================================
# CORE PROCESSOR
# ============================================================
def process_all_files():
    stats = {
        "files": 0,
        "rows": 0,
        "valid": 0,
        "invalid": 0,
        "quantity": 0,
        "revenue": 0,
        "by_product": defaultdict(lambda: {"qty": 0, "rev": 0}),
        "by_date": defaultdict(lambda: {"qty": 0, "rev": 0}),
    }

    files = [f for f in os.listdir(DATA_IN) if f.endswith(".csv")]
    if not files:
        return {"processed": 0}

    for filename in files:
        stats["files"] += 1
        filepath = os.path.join(DATA_IN, filename)
        error_count = 0

        logging.info(f"Processing file: {filename}")

        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for raw_row in reader:
                stats["rows"] += 1

                # Normalize headers (CRITICAL FIX)
                row = normalize_row(raw_row)

                if not validate_row(row):
                    stats["invalid"] += 1
                    error_count += 1
                    continue

                stats["valid"] += 1

                qty = int(row["quantity"])
                price = float(row["price"])
                revenue = qty * price

                stats["quantity"] += qty
                stats["revenue"] += revenue

                # ---- Aggregations ----
                stats["by_product"][row["product"]]["qty"] += qty
                stats["by_product"][row["product"]]["rev"] += revenue

                stats["by_date"][row["date"]]["qty"] += qty
                stats["by_date"][row["date"]]["rev"] += revenue

        # ---- Move file based on error threshold ----
        target_dir = DATA_ERR if error_count > ERROR_THRESHOLD else DATA_OUT
        os.rename(filepath, os.path.join(target_dir, filename))

        logging.info(
            f"File done | {filename} | "
            f"errors={error_count}"
        )

    # ---- Write analytical reports ----
    write_reports(RUN_ID, stats)

    logging.info(
        f"Run summary | files={stats['files']} rows={stats['rows']} "
        f"valid={stats['valid']} invalid={stats['invalid']} "
        f"qty={stats['quantity']} revenue={stats['revenue']}"
    )

    return {
        "processed": stats["files"],
        "out": stats["files"],
        "err": stats["invalid"]
    }
