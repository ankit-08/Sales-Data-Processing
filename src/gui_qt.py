import sys
import os

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel,
    QVBoxLayout, QWidget, QTextEdit, QCheckBox, QComboBox
)
from PySide6.QtCore import QTimer

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

from test_data_create.generate_test_csv import (
    start_csv_generator, stop_csv_generator
)

from .main import (
    configure_logging,
    start_file_processing,
    stop_file_processing,
)

from .analytics.plots import load_by_product


# ============================================================
# PATHS
# ============================================================
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(PROJECT_ROOT, "logs", "system.log")
REPORT_DIR = os.path.join(PROJECT_ROOT, "src", "reports")


# ============================================================
# STYLES
# ============================================================
ACTIVE_GREEN = """
QPushButton {
    background-color: #6fcf97;
    color: white;
    font-weight: 600;
}
"""

DANGER_RED = """
QPushButton {
    background-color: #eb5757;
    color: white;
    font-weight: 600;
}
"""


# ============================================================
# GUI
# ============================================================
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Data Processor")

        self.generator_running = False
        self.processing_running = False

        # ---------------- STATUS ----------------
        self.status = QLabel("Status: Idle")

        # ---------------- CONTROLS ----------------
        self.log_console_toggle = QCheckBox("Print logs in terminal")
        self.log_console_toggle.setChecked(True)

        self.level_select = QComboBox()
        self.level_select.addItems(["ALL", "INFO", "WARNING", "ERROR"])
        self.level_select.setCurrentText("ALL")

        # ---------------- BUTTONS ----------------
        self.start_gen = QPushButton("Start CSV Generator")
        self.stop_gen = QPushButton("Stop CSV Generator")

        self.start_proc = QPushButton("Start File Processing")
        self.stop_proc = QPushButton("Stop File Processing")

        self.clear_log_btn = QPushButton("Clear Logs")
        self.exit_btn = QPushButton("Stop Program")
        self.exit_btn.setStyleSheet(DANGER_RED)

        # ---------------- LOG VIEW ----------------
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)

        # ---------------- CHART ----------------
        self.figure = Figure(figsize=(9, 4.5))
        self.ax = self.figure.add_subplot(111)
        self.chart = FigureCanvasQTAgg(self.figure)

        # ---------------- SIGNALS ----------------
        self.start_gen.clicked.connect(self.start_generator)
        self.stop_gen.clicked.connect(self.stop_generator)
        self.start_proc.clicked.connect(self.start_processing)
        self.stop_proc.clicked.connect(self.stop_processing)
        self.clear_log_btn.clicked.connect(self.clear_logs)
        self.exit_btn.clicked.connect(self.stop_program)

        # ---------------- LAYOUT ----------------
        layout = QVBoxLayout()
        layout.addWidget(self.status)
        layout.addWidget(self.log_console_toggle)
        layout.addWidget(QLabel("Log Filter (Viewer Only)"))
        layout.addWidget(self.level_select)

        layout.addWidget(self.start_gen)
        layout.addWidget(self.stop_gen)
        layout.addWidget(self.start_proc)
        layout.addWidget(self.stop_proc)
        layout.addWidget(self.clear_log_btn)
        layout.addWidget(self.exit_btn)

        layout.addWidget(QLabel("Logs"))
        layout.addWidget(self.log_view)

        layout.addWidget(QLabel("Live Revenue Dashboard"))
        layout.addWidget(self.chart)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # ---------------- TIMER ----------------
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_logs)
        self.timer.timeout.connect(self.refresh_chart)
        self.timer.start(3000)

    # ========================================================
    # GENERATOR CONTROL
    # ========================================================
    def start_generator(self):
        if self.generator_running:
            return
        configure_logging(self.log_console_toggle.isChecked(), "INFO")
        start_csv_generator()
        self.generator_running = True
        self.status.setText("Status: Generator Running")
        self.start_gen.setStyleSheet(ACTIVE_GREEN)

    def stop_generator(self):
        stop_csv_generator()
        self.generator_running = False
        self.status.setText("Status: Generator Stopped")
        self.start_gen.setStyleSheet("")

    # ========================================================
    # PROCESSING CONTROL
    # ========================================================
    def start_processing(self):
        if self.processing_running:
            return
        configure_logging(self.log_console_toggle.isChecked(), "INFO")
        start_file_processing()
        self.processing_running = True
        self.status.setText("Status: Processing Running")
        self.start_proc.setStyleSheet(ACTIVE_GREEN)

    def stop_processing(self):
        stop_file_processing()
        self.processing_running = False
        self.status.setText("Status: Processing Stopped")
        self.start_proc.setStyleSheet("")

    # ========================================================
    # LOG VIEWER
    # ========================================================
    def refresh_logs(self):
        if not os.path.exists(LOG_FILE):
            return

        selected = self.level_select.currentText()
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if selected != "ALL":
            lines = [l for l in lines if f"[{selected}]" in l]

        self.log_view.setPlainText("".join(lines))
        self.log_view.verticalScrollBar().setValue(
            self.log_view.verticalScrollBar().maximum()
        )

    # ========================================================
    # LIVE CHART (FIXED)
    # ========================================================
    def refresh_chart(self):
        self.ax.clear()

        df = load_by_product(REPORT_DIR)
        if df.empty:
            self.ax.set_title("Waiting for data...", color="white")
            self.chart.draw()
            return

        df = df.sort_values("total_revenue", ascending=False).head(10)

        products = df["product"]
        revenue = df["total_revenue"]

        # ---- Theme ----
        self.figure.patch.set_facecolor("#0b1220")
        self.ax.set_facecolor("#0b1220")

        # ---- Bars (FIXED WIDTH) ----
        self.ax.bar(
            products,
            revenue,
            width=0.55,
            color="#e5e7eb"
        )

        # ---- Levels ----
        max_rev = revenue.max()
        levels = {
            "LOW": max_rev * 0.3,
            "MEDIUM": max_rev * 0.6,
            "HIGH": max_rev * 0.9,
        }

        for label, y in levels.items():
            self.ax.axhline(y=y, linestyle="--", color="#64748b", linewidth=1)
            self.ax.text(
                0.02,
                y / max_rev,
                label,
                transform=self.ax.transAxes,
                color="#94a3b8",
                fontsize=9,
                va="bottom"
            )

        # ---- Y-axis formatting (NO scientific notation) ----
        self.ax.yaxis.set_major_formatter(
            FuncFormatter(lambda x, _: f"₹{x/1_000_000:.1f}M")
        )

        # ---- Cleanup ----
        self.ax.set_title("Revenue Levels by Product", color="white", pad=12)
        self.ax.set_ylabel("Revenue (Millions)", color="white")
        self.ax.tick_params(axis="x", colors="white", rotation=35)
        self.ax.tick_params(axis="y", colors="white")

        for spine in self.ax.spines.values():
            spine.set_visible(False)

        self.figure.tight_layout()
        self.chart.draw()

    # ========================================================
    # CLEAR LOGS
    # ========================================================
    def clear_logs(self):
        if os.path.exists(LOG_FILE):
            open(LOG_FILE, "w").close()
        self.log_view.clear()
        self.status.setText("Status: Logs Cleared")

    # ========================================================
    # STOP PROGRAM
    # ========================================================
    def stop_program(self):
        stop_csv_generator()
        stop_file_processing()
        self.status.setText("Status: Program Stopped")
        QApplication.quit()


# ============================================================
# ENTRY
# ============================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec())
