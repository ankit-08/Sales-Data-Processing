# Sales-Data-Processing
Read daily sales data from text/CSV files, clean it, summarize totals, and write reports.

#Input File Format: .CSV
    product_name, catagory, quantity, price

#Reading Rules: 
    product_name: string
    catagory: string
    quantity: float
    price: float
    
#Transaformation Logic:
    Aggregates metrics: total revenue, product-wise revenue, product-wise quantity sold, daily totals.
    Generates human-readable reports (text/CSV) and a summary JSON.
    Supports incremental updates (append new daily files) and error logging.

Step 1 :: Activate the venv
    cd /workspaces/Sales-Data-Processing
    source .venv/bin/activate
Step 2 :: Activate GUI 
    cd /workspaces/Sales-Data-Processing
    python -m src.gui_qt

If Step 2 through error
sudo apt update
sudo apt install -y libgl1 libglib2.0-0
