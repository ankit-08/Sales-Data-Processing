import os
import csv
import random
import time
import threading
import logging
from datetime import datetime, timedelta

# ============================================================
# CONFIG
# ============================================================
INTERVAL_SECONDS = 2
ROWS_PER_FILE = 100
START_DATE = datetime(2025, 11, 1)

PRODUCTS = [
    "Samsung 55-inch LED TV",
    "LG Smart Refrigerator",
    "Apple iPhone 15",
    "OnePlus Nord CE 5G",
    "Sony Noise-Cancelling Headphones",
    "Dell Inspiron Laptop",
    "HP Pavilion Laptop",
    "Xiaomi Mi 11 Mobile",
    "Whirlpool Washing Machine",
    "Bosch Dishwasher",
    "Panasonic Microwave Oven",
    "Philips Air Purifier",
    "Bajaj Mixer Grinder",
    "LG Air Conditioner",
    "Haier Deep Freezer",
    "Canon DSLR Camera",
    "Lenovo Tablet",
    "Boat Bluetooth Speaker",
    "Samsung Galaxy Watch",
    "Apple iPad Air"
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "in")
os.makedirs(OUTPUT_DIR, exist_ok=True)

_stop_flag = threading.Event()

# ============================================================
def _generate_row():
    date = (START_DATE + timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
    product = random.choice(PRODUCTS)
    qty = random.randint(1, 10)
    price = random.randint(1000, 50000)
    return [date, product, qty, price]

def _run_generator():
    logging.info("CSV generator started")
    while not _stop_flag.is_set():
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"sales_{ts}.csv"
        path = os.path.join(OUTPUT_DIR, fname)

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "product", "qty", "price"])
            for _ in range(ROWS_PER_FILE):
                writer.writerow(_generate_row())

        logging.info(f"Generated CSV file: {fname}")

        for _ in range(INTERVAL_SECONDS):
            if _stop_flag.is_set():
                break
            time.sleep(1)

    logging.info("CSV generator stopped")

def start_csv_generator():
    _stop_flag.clear()
    threading.Thread(target=_run_generator, daemon=True).start()

def stop_csv_generator():
    _stop_flag.set()
    logging.info("Stop CSV generator requested")
