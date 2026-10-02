"""Reference solution: UCI Online Retail transaction and customer analysis."""

import matplotlib.pyplot as plt
import pandas as pd

from ds301 import load_dataset
from ds301.paths import data_path
from ds301.reporting import ensure_output, save_figure

path = data_path("open/online_retail/data.csv")
if not path.exists():
    load_dataset("online_retail")
data = pd.read_csv(path)
data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"])
data["is_cancellation"] = data["InvoiceNo"].astype(str).str.upper().str.startswith("C")
data["line_value"] = data["Quantity"] * data["UnitPrice"]
print("rows", len(data), "invoices", data["InvoiceNo"].nunique())
print("cancellation-line rate", data["is_cancellation"].mean())

sales = data.loc[(data["Quantity"] > 0) & (data["UnitPrice"] > 0)].copy()
snapshot = sales["InvoiceDate"].max() + pd.Timedelta(days=1)
rfm = sales.groupby("CustomerID").agg(
    recency=("InvoiceDate", lambda x: (snapshot - x.max()).days),
    frequency=("InvoiceNo", "nunique"),
    monetary=("line_value", "sum"),
)
rfm.to_csv(ensure_output("assignment03_retail") / "rfm.csv")

monthly = sales.set_index("InvoiceDate")["line_value"].resample("MS").sum()
monthly.plot(color="#006D77", marker="o")
plt.ylabel("Observed sales value (GBP)")
plt.title("UCI Online Retail: monthly positive-quantity sales")
save_figure(ensure_output("assignment03_retail") / "monthly_sales.png")
