"""Reference structure for the end-to-end decision project."""

import pandas as pd

from ds301.paths import data_path
from ds301.reporting import audit_table, ensure_output

path = data_path("synthetic_customer_operations/customer_operations.csv")
data = pd.read_csv(path, parse_dates=["order_date"])
clean = data.drop_duplicates("order_id").copy()
clean["late_over_30"] = clean["delivery_minutes"] > 30
decision_table = clean.groupby(["region", "campaign_period"], observed=True).agg(
    orders=("order_id", "nunique"),
    late_rate=("late_over_30", "mean"),
    return_rate=("returned", "mean"),
    median_delivery=("delivery_minutes", "median"),
)
out = ensure_output("assignment08_capstone")
audit_table(data).to_csv(out / "audit.csv")
decision_table.to_csv(out / "decision_table.csv")
print(decision_table)
print(
    "Reference recommendation: investigate campaign-period capacity and pilot a targeted "
    "staffing or promise-setting change; monitor late rate, returns, cost and regional service."
)
