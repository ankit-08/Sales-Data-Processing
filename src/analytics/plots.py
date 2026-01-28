import os
import pandas as pd
import seaborn as sns

def load_by_product(report_dir):
    path = os.path.join(report_dir, "by_product.csv")
    if not os.path.exists(path):
        return pd.DataFrame()

    df = pd.read_csv(path)

    # Aggregate across runs
    return (
        df.groupby("product", as_index=False)
          .agg(total_quantity=("total_quantity", "sum"),
               total_revenue=("total_revenue", "sum"))
    )

def load_by_date(report_dir):
    path = os.path.join(report_dir, "by_date.csv")
    if not os.path.exists(path):
        return pd.DataFrame()

    df = pd.read_csv(path)

    return (
        df.groupby("date", as_index=False)
          .agg(total_revenue=("total_revenue", "sum"))
          .sort_values("date")
    )
