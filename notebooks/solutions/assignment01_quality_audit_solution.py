"""Reference solution: data contract and quality audit."""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from ds301.paths import data_path
from ds301.reporting import audit_table, ensure_output, save_figure

DATA = data_path("synthetic_customer_operations/customer_operations.csv")
out = ensure_output("assignment01_quality")
data = pd.read_csv(DATA, parse_dates=["order_date"])

audit_table(data).to_csv(out / "field_audit.csv")
duplicate_orders = data.duplicated("order_id", keep=False)
print("rows", len(data), "unique orders", data["order_id"].nunique())
print("duplicate rows", int(duplicate_orders.sum()))
print("missing satisfaction", int(data["satisfaction_1_to_5"].isna().sum()))

missing_by_return = (
    data.assign(missing_satisfaction=data["satisfaction_1_to_5"].isna())
    .groupby("returned", observed=True)["missing_satisfaction"]
    .agg(["count", "mean"])
)
missing_by_return.to_csv(out / "missingness_by_return.csv")

clean = data.drop_duplicates("order_id", keep="first")
before = data["order_value_inr"].sum()
after = clean["order_value_inr"].sum()
print(f"order-value reconciliation: before={before:,.2f}; after={after:,.2f}")

sns.barplot(data=clean, x="region", y="delivery_minutes", estimator="median", errorbar=None)
plt.ylabel("Median delivery time (minutes)")
plt.title("Synthetic operations: median delivery time by region")
save_figure(out / "delivery_by_region.png")
