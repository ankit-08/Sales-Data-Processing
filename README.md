# Sales-Data-Processing

A Python-based **Sales Data Processing System** with:
- CSV data validation
- Aggregation & reporting
- Error-threshold handling
- Modern GUI (Start / Stop buttons with live logs)
- CLI support for automation

Designed using **real-world ETL & data engineering practices**.

---

## ✨ Features

### 🧪 Data Creation
- Generate test CSV files
- Start / Stop generation from GUI
- Live logs displayed in UI

### ⚙️ Data Processing
- Validate and process sales CSV files
- Aggregate:
  - Total revenue
  - Product-wise quantity & revenue
  - Daily totals
- File handling based on error threshold:
  - `<= 5` row errors → processed successfully
  - `> 5` row errors → moved to error folder
- Live logs in GUI
- CLI mode for automation

---

## 📁 Project Structure

Sales-Data-Processing/
├── src/
│ ├── init.py
│ ├── main.py # CLI entry point
│ ├── gui_qt.py # PySide6 GUI
│ ├── processor.py # Core processing logic
│ ├── io_utils.py # File I/O helpers
│ └── validators.py # Row validation
│
├── test_data_create/
│ └── generate_test_csv.py
│
├── tests/
│ ├── conftest.py
│ ├── test_processor.py
│ └── test_error_thresholds.py
│
├── data/
│ ├── in/ # Incoming CSVs
│ ├── out/ # Successfully processed files
│ └── err/ # Files with > threshold errors
│
├── reports/ # Generated reports
├── logs/ # system.log
├── requirements.txt
└── README.md

yaml
Copy code

---

## ⚙️ Prerequisites

- Python **3.11 or 3.12**
- Windows / macOS / Linux
- Local VS Code (GUI is **not supported** in Codespaces)

---

# 🚀 STEP-BY-STEP: FIRST TIME SETUP

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd Sales-Data-Processing
2️⃣ Create Virtual Environment
bash
Copy code
python -m venv .venv
3️⃣ Activate Virtual Environment
Windows

bat
Copy code
.venv\Scripts\activate
macOS / Linux

bash
Copy code
source .venv/bin/activate
You should see:

scss
Copy code
(.venv)
4️⃣ Select Python Interpreter in VS Code (IMPORTANT)
Open VS Code

Press Ctrl + Shift + P

Select Python: Select Interpreter

Choose:

bash
Copy code
.venv/Scripts/python.exe
5️⃣ Install Dependencies
bash
Copy code
pip install --upgrade pip
pip install -r requirements.txt
pip install pyside6
6️⃣ Run Unit Tests (Sanity Check)
bash
Copy code
pytest
▶️ STARTING THE PROJECT
🖥️ GUI Mode (Recommended)
bash
Copy code
python -m src.gui_qt
GUI provides:
Data Creation Section

Start / Stop button

Live logs

Data Processing Section

Start / Stop button

Live logs

🧾 CLI Mode (Without GUI)
bash
Copy code
python -m src.main
Use CLI mode for:

Automation

Scheduled jobs

CI/CD pipelines

🔁 DAILY USAGE (VERY IMPORTANT)
Every time you start working on the project:

bash
Copy code
cd Sales-Data-Processing
.venv\Scripts\activate
code .
Then run:

GUI → python -m src.gui_qt

Tests → pytest

CLI → python -m src.main

📊 Output