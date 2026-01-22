import os
import shutil
import logging
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

INPUT_DIR = os.path.join(DATA_DIR, "in")
OUTPUT_DIR = os.path.join(DATA_DIR, "out")
ERROR_DIR = os.path.join(DATA_DIR, "err")

for d in (INPUT_DIR, OUTPUT_DIR, ERROR_DIR):
    os.makedirs(d, exist_ok=True)

def get_input_files():
    return [
        os.path.join(INPUT_DIR, f)
        for f in os.listdir(INPUT_DIR)
        if f.endswith(".csv")
    ]

def _move(src, dest_dir):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = os.path.basename(src)
    dest = os.path.join(dest_dir, f"{name}_{ts}")
    shutil.move(src, dest)
    return os.path.basename(dest)

def move_to_processed(path, errors):
    name = _move(path, OUTPUT_DIR)
    logging.info(f"Moved to OUT: {name} | errors={errors}")

def move_to_error(path, errors):
    name = _move(path, ERROR_DIR)
    logging.error(f"Moved to ERR: {name} | errors={errors}")
