"""Reference solution: UCI Bike Sharing forecasting baselines and capacity reasoning."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error

from ds301 import load_dataset
from ds301.paths import data_path
from ds301.reporting import ensure_output, save_figure

path = data_path("open/bike_sharing/data.csv")
if not path.exists():
    load_dataset("bike_sharing")
data = pd.read_csv(path)
date_col = "dteday" if "dteday" in data else next(c for c in data if "date" in c.lower())
target = "cnt" if "cnt" in data else next(c for c in data if c.lower() in {"count", "target"})
data[date_col] = pd.to_datetime(data[date_col])
if "hr" in data:
    data["timestamp"] = data[date_col] + pd.to_timedelta(data["hr"], unit="h")
    grain = "hour"
    seasonal_lag = 24 * 7
else:
    data["timestamp"] = data[date_col]
    grain = "day"
    seasonal_lag = 7

series = (
    data.groupby("timestamp", as_index=False)[target]
    .sum()
    .sort_values("timestamp")
    .set_index("timestamp")
    .asfreq("h" if grain == "hour" else "D")
)
print("forecast grain", grain)
print("observed rows", series[target].notna().sum())
print("missing periods after regularisation", series[target].isna().sum())

# Baselines use only values available before the forecasted period.
series["last_value"] = series[target].shift(1)
series["seasonal_naive"] = series[target].shift(seasonal_lag)
holdout_start = series.index[int(len(series) * 0.80)]
holdout = series.loc[holdout_start:].dropna(subset=[target, "last_value", "seasonal_naive"])


def error_row(name: str, prediction: pd.Series) -> dict[str, float | str]:
    error = holdout[target] - prediction
    return {
        "model": name,
        "MAE": mean_absolute_error(holdout[target], prediction),
        "RMSE": float(np.sqrt(np.mean(np.square(error)))),
        "bias_actual_minus_forecast": float(error.mean()),
    }


metrics = pd.DataFrame(
    [
        error_row("last value", holdout["last_value"]),
        error_row("weekly seasonal naive", holdout["seasonal_naive"]),
    ]
)
print("chronological holdout begins", holdout_start)
print(metrics.to_string(index=False))
output = ensure_output("assignment02_time_series")
metrics.to_csv(output / "baseline_metrics.csv", index=False)

monthly = series[target].resample("MS").mean()
monthly.plot(marker="o", color="#006D77")
plt.ylabel(f"Mean {grain}ly rentals")
plt.title("UCI Bike Sharing: monthly demand level")
save_figure(output / "monthly_demand.png")

display_periods = 24 * 7 if grain == "hour" else 35
holdout.tail(display_periods)[[target, "last_value", "seasonal_naive"]].plot(
    figsize=(10, 4.8), color=["#123B4A", "#E29520", "#83C5BE"], linewidth=1.4
)
plt.ylabel("Rental count")
plt.title("Actual demand and two honest baselines in the final holdout window")
save_figure(output / "holdout_baselines.png")

if "hr" in data:
    profile_columns = ["hr"]
    if "workingday" in data:
        profile_columns.append("workingday")
    profile = data.groupby(profile_columns, as_index=False)[target].mean()
    if "workingday" in profile:
        for workingday, frame in profile.groupby("workingday"):
            plt.plot(
                frame["hr"],
                frame[target],
                marker="o",
                label=f"workingday={workingday}",
            )
        plt.legend()
    else:
        plt.plot(profile["hr"], profile[target], marker="o")
    plt.xlabel("Hour")
    plt.ylabel("Mean rentals")
    plt.title("Demand shape reveals the capacity-relevant hours")
    save_figure(output / "hourly_profile.png")

print(
    "Decision interpretation: positive bias under the stated convention means average "
    "underforecasting. A capacity policy should test shortage and holding costs, peak errors, "
    "and interval coverage; the baseline comparison alone does not choose fleet capacity."
)
