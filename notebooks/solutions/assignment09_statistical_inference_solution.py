"""Reference solution: estimator uncertainty and bootstrap reasoning."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ds301.paths import data_path
from ds301.reporting import ensure_output

path = data_path("synthetic_customer_operations/customer_operations.csv")
data = pd.read_csv(path)
regions = data["region"].dropna().value_counts().index[:2].tolist()
if len(regions) < 2:
    raise ValueError("At least two regions are required")

first = data.loc[data["region"].eq(regions[0]), "delivery_minutes"].dropna().to_numpy()
second = data.loc[data["region"].eq(regions[1]), "delivery_minutes"].dropna().to_numpy()
estimate = float(first.mean() - second.mean())

rng = np.random.default_rng(301)
replicates = np.empty(5_000)
for index in range(len(replicates)):
    first_star = rng.choice(first, size=len(first), replace=True)
    second_star = rng.choice(second, size=len(second), replace=True)
    replicates[index] = first_star.mean() - second_star.mean()

lower, upper = np.quantile(replicates, [0.025, 0.975])
summary = pd.DataFrame(
    {
        "contrast": [f"{regions[0]} minus {regions[1]}"],
        "mean_difference_minutes": [estimate],
        "bootstrap_2.5_percentile": [lower],
        "bootstrap_97.5_percentile": [upper],
        "replicates": [len(replicates)],
    }
)
output = ensure_output("assignment09_inference")
summary.to_csv(output / "bootstrap_summary.csv", index=False)

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hist(replicates, bins=45, color="#83c5be", edgecolor="white")
ax.axvline(estimate, color="#123b4a", linewidth=2.5, label="Observed difference")
ax.axvspan(lower, upper, color="#e29520", alpha=0.25, label="95% percentile interval")
ax.set(
    title="Bootstrap distribution of a regional mean difference",
    xlabel="Mean delivery-time difference (minutes)",
    ylabel="Bootstrap replicates",
)
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(output / "bootstrap_distribution.png", dpi=180)
print(summary.to_string(index=False))
print("Interpretation: descriptive process contrast; not a causal regional effect.")
