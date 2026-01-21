import sys
import threading
import logging
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QTextEdit,
    QLabel, QVBoxLayout, QHBoxLayout, QGroupBox
)
from PySide6.QtCore import Qt, Signal, QObject

from src.main import main as run_processor
from test_data_create.generate_test_csv import generate_csv_files

# ---------- Logging Bridge ----------
class QtLogHandler(logging.Handler, QObject):
    log_signal = Signal(str)

    def __init__(self):
        logging.Handler.__init__(self)
        QObject.__init__(self)

    def emit(self, record):
        msg = self.format(record)
        self.log_signal.emit(msg)

# ---------- Worker Base ----------
class StoppableWorker(threading.Thread):
    def __init__(self, target, log_fn):
        super().__init__(daemon=True)
        self._stop_event = threading.Event()
        self.target = target
        self.log_fn = log_fn

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

# ---------- GUI ----------
class SalesGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Data Processing System")
        self.setMinimumSize(900, 500)
        self.setWindowOpacity(0.94)

        self.data_gen_worker = None
        self.data_proc_worker = None

        self.init_ui()
        self.init_logging()

    # ---------- UI ----------
    def init_ui(self):
        main_layout = QHBoxLayout(self)

        # ---- Data Creation Section ----
        self.gen_log = QTextEdit()
        self.gen_log.setReadOnly(True)

        self.gen_btn = QPushButton("▶ Start Data Creation")
        self.gen_btn.clicked.connect(self.toggle_data_creation)

        gen_box = QGroupBox("🧪 Data Creation")
        gen_layout = QVBoxLayout()
        gen_layout.addWidget(self.gen_btn)
        gen_layout.addWidget(self.gen_log)
        gen_box.setLayout(gen_layout)

        # ---- Data Processing Section ----
        self.proc_log = QTextEdit()
        self.proc_log.setReadOnly(True)

        self.proc_btn = QPushButton("▶ Start Data Processing")
        self.proc_btn.clicked.connect(self.toggle_data_processing)

        proc_box = QGroupBox("⚙️ Data Processing")
        proc_layout = QVBoxLayout()
        proc_layout.addWidget(self.proc_btn)
        proc_layout.addWidget(self.proc_log)
        proc_box.setLayout(proc_layout)

        main_layout.addWidget(gen_box)
        main_layout.addWidget(proc_box)

    # ---------- Logging ----------
    def init_logging(self):
        self.log_handler = QtLogHandler()
        self.log_handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        )
        self.log_handler.log_signal.connect(self.route_log)

        root = logging.getLogger()
        root.setLevel(logging.INFO)
        root.addHandler(self.log_handler)

    def route_log(self, message):
        if "generate" in message.lower():
            self.gen_log.append(message)
        else:
            self.proc_log.append(message)

    # ---------- Data Creation ----------
    def toggle_data_creation(self):
        if self.data_gen_worker and self.data_gen_worker.is_alive():
            self.data_gen_worker.stop()
            self.gen_btn.setText("▶ Start Data Creation")
            self.gen_log.append("⛔ Data creation stopped.")
        else:
            self.gen_log.append("▶ Data creation started...")
            self.gen_btn.setText("⛔ Stop Data Creation")
            self.data_gen_worker = StoppableWorker(
                target=self.run_data_creation,
                log_fn=self.gen_log.append
            )
            self.data_gen_worker.start()

    def run_data_creation(self):
        try:
            generate_csv_files()
            self.gen_log.append("✅ Data creation completed.")
        except Exception as e:
            self.gen_log.append(f"❌ Error: {e}")

    # ---------- Data Processing ----------
    def toggle_data_processing(self):
        if self.data_proc_worker and self.data_proc_worker.is_alive():
            self.proc_log.append("⛔ Stop requested. Finishing current file...")
            self.proc_btn.setText("▶ Start Data Processing")
        else:
            self.proc_log.append("▶ Data processing started...")
            self.proc_btn.setText("⛔ Stop Data Processing")
            self.data_proc_worker = threading.Thread(
                target=self.run_processing,
                daemon=True
            )
            self.data_proc_worker.start()

    def run_processing(self):
        try:
            run_processor()
            self.proc_log.append("✅ Data processing completed.")
        except Exception as e:
            self.proc_log.append(f"❌ Error: {e}")
        finally:
            self.proc_btn.setText("▶ Start Data Processing")

# ---------- Entry ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = SalesGUI()
    gui.show()
    sys.exit(app.exec())
