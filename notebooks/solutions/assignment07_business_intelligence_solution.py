"""Reference solution: public-indicator BI using the World Bank API."""

import matplotlib.pyplot as plt
import pandas as pd

from ds301 import load_dataset
from ds301.paths import data_path
from ds301.reporting import ensure_output, save_figure

path = data_path("open/world_bank_india/data.csv")
if not path.exists():
    load_dataset("world_bank_india")
data = pd.read_csv(path)
pivot = data.pivot(index="year", columns="indicator", values="value").sort_index()
pivot.to_csv(ensure_output("assignment07_bi") / "indicator_table.csv")
cols = [c for c in pivot if "Internet" in c or "Urban" in c]
pivot[cols].plot(marker="o")
plt.ylabel("Percent")
plt.title("India: selected World Development Indicators")
plt.legend(fontsize=8)
save_figure(ensure_output("assignment07_bi") / "india_indicators.png")
