import os
import sys
import time
import threading
import logging

from .context import RUN_ID
from .processor import process_all_files

# ================= PATHS =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "system.log")

_stop_event = threading.Event()

# ================= LOG RECORD =================
_old_factory = logging.getLogRecordFactory()

def record_factory(*args, **kwargs):
    record = _old_factory(*args, **kwargs)
    record.run_id = RUN_ID
    return record

logging.setLogRecordFactory(record_factory)

# ================= EMOJI FORMATTER =================
EMOJI = {
    logging.INFO: "ℹ️",
    logging.WARNING: "⚠️",
    logging.ERROR: "🚫",
    logging.CRITICAL: "🚫",
}

class EmojiFormatter(logging.Formatter):
    def format(self, record):
        msg = str(record.msg)
        for e in EMOJI.values():
            if msg.startswith(e):
                msg = msg[len(e):].lstrip()
        record.msg = f"{EMOJI.get(record.levelno, '')} {msg}"
        return super().format(record)

# ================= LOGGING =================
LEVELS = {
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
}

def configure_logging(print_console=True, level="INFO"):
    root = logging.getLogger()
    root.setLevel(LEVELS.get(level, logging.INFO))
    root.handlers.clear()

    formatter = EmojiFormatter(
        "%(asctime)s [%(levelname)s] RunID=%(run_id)s | %(message)s"
    )

    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setFormatter(formatter)
    root.addHandler(fh)

    if print_console:
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        root.addHandler(ch)

    logging.info("Logging initialized")

# ================= PROCESS LOOP =================
def _processor_loop():
    logging.info("Sales Data Processor started")

    while not _stop_event.is_set():
        summary = process_all_files()
        if summary.get("processed", 0) == 0:
            logging.warning("No CSV files found")
        time.sleep(2)

    logging.info("Sales Data Processor stopped")

# ================= PUBLIC API =================
def start_file_processing():
    _stop_event.clear()
    threading.Thread(target=_processor_loop, daemon=True).start()

def stop_file_processing():
    _stop_event.set()
    logging.info("Stop file processing requested")
