"""Generate documented synthetic operations, duration, and experiment datasets.

The generator deliberately includes missing satisfaction values, a small number
of duplicate identifiers, campaign periods and region-specific demand. It is
synthetic: no record represents a real customer, employee or organisation.
"""

from __future__ import annotations

import json

import numpy as np
import pandas as pd

from ds301.paths import data_path

SEED = 301


def main() -> None:
    rng = np.random.default_rng(SEED)
    n = 1800
    dates = pd.date_range("2025-01-01", "2025-06-30", freq="D")
    order_date = pd.to_datetime(rng.choice(dates, n))
    region = rng.choice(["East", "West", "North", "South"], n, p=[0.24, 0.21, 0.29, 0.26])
    channel = rng.choice(["App", "Web", "Store"], n, p=[0.46, 0.31, 0.23])
    category = rng.choice(
        ["Grocery", "Home", "Personal Care", "Electronics"], n, p=[0.42, 0.24, 0.22, 0.12]
    )
    campaign = ((order_date.month == 3) | (order_date.month == 6)).astype(int)
    base_value = {"Grocery": 850, "Home": 1450, "Personal Care": 650, "Electronics": 4800}
    amount = np.array([base_value[x] for x in category]) * rng.lognormal(0, 0.38, n)
    delay = np.maximum(0, rng.normal(18, 8, n) + 5 * (region == "East") + 7 * campaign)
    returned = rng.binomial(
        1, np.clip(0.035 + 0.0008 * delay + 0.025 * (channel == "Web"), 0, 0.35)
    )
    satisfaction = np.clip(np.rint(5.2 - delay / 13 - 1.1 * returned + rng.normal(0, 0.7, n)), 1, 5)
    satisfaction[rng.random(n) < (0.09 + 0.08 * returned)] = np.nan
    frame = pd.DataFrame(
        {
            "order_id": [f"O{100000 + i}" for i in range(n)],
            "customer_id": [f"C{v:04d}" for v in rng.integers(1, 601, n)],
            "order_date": order_date,
            "region": region,
            "channel": channel,
            "category": category,
            "campaign_period": campaign,
            "order_value_inr": np.round(amount, 2),
            "delivery_minutes": np.round(delay, 1),
            "returned": returned,
            "satisfaction_1_to_5": satisfaction,
        }
    ).sort_values("order_date")
    duplicates = frame.sample(9, random_state=SEED)
    frame = pd.concat([frame, duplicates], ignore_index=True).sort_values("order_date")

    folder = data_path("synthetic_customer_operations")
    folder.mkdir(parents=True, exist_ok=True)
    frame.to_csv(folder / "customer_operations.csv", index=False)
    metadata = {
        "title": "Synthetic customer operations",
        "generator": "scripts/generate_synthetic.py",
        "seed": SEED,
        "rows": len(frame),
        "real_people": False,
        "designed_features": [
            "campaign-related demand and delay",
            "regional delay variation",
            "return-related satisfaction missingness",
            "nine duplicated order records",
        ],
    }
    (folder / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"wrote {len(frame):,} rows to {folder / 'customer_operations.csv'}")

    n_duration = 1400
    plan = rng.choice(["Basic", "Plus", "Premium"], n_duration, p=[0.48, 0.34, 0.18])
    acquisition = rng.choice(["Organic", "Partner", "Paid"], n_duration, p=[0.44, 0.24, 0.32])
    support_contacts = rng.poisson(1.4, n_duration)
    monthly_value = np.round(
        rng.lognormal(4.0, 0.35, n_duration)
        * np.select([plan == "Plus", plan == "Premium"], [1.35, 2.1], default=1.0),
        2,
    )
    daily_hazard = 0.0015 * np.exp(
        0.16 * support_contacts
        + 0.28 * (acquisition == "Paid")
        - 0.25 * (plan == "Plus")
        - 0.48 * (plan == "Premium")
    )
    latent_event_days = rng.exponential(1 / daily_hazard)
    censor_days = rng.uniform(150, 720, n_duration)
    observed_days = np.ceil(np.minimum(latent_event_days, censor_days)).astype(int)
    event_churn = (latent_event_days <= censor_days).astype(int)
    duration = pd.DataFrame(
        {
            "subscriber_id": [f"S{index:05d}" for index in range(1, n_duration + 1)],
            "plan": plan,
            "acquisition_channel": acquisition,
            "support_contacts_first_30d": support_contacts,
            "monthly_value_inr": monthly_value,
            "observed_days": observed_days,
            "event_churn": event_churn,
        }
    )
    duration_folder = data_path("synthetic_subscription_duration")
    duration_folder.mkdir(parents=True, exist_ok=True)
    duration.to_csv(duration_folder / "subscription_duration.csv", index=False)
    duration_metadata = {
        "title": "Synthetic subscription duration",
        "generator": "scripts/generate_synthetic.py",
        "seed": SEED,
        "rows": len(duration),
        "real_people": False,
        "event": "designed voluntary churn event",
        "censoring": "independent administrative follow-up conditional on generated fields",
    }
    (duration_folder / "metadata.json").write_text(
        json.dumps(duration_metadata, indent=2), encoding="utf-8"
    )
    print(f"wrote {len(duration):,} rows to {duration_folder / 'subscription_duration.csv'}")

    n_experiment = 8000
    treatment = np.repeat([0, 1], n_experiment // 2)
    rng.shuffle(treatment)
    device = rng.choice(["Mobile", "Desktop"], n_experiment, p=[0.68, 0.32])
    exp_region = rng.choice(["East", "West", "North", "South"], n_experiment)
    prior_tasks = rng.poisson(2.3, n_experiment)
    baseline = (
        0.19
        + 0.032 * (device == "Desktop")
        + 0.018 * (exp_region == "West")
        + 0.012 * np.minimum(prior_tasks, 5)
    )
    uplift = 0.012 + 0.017 * (device == "Mobile") - 0.008 * (prior_tasks >= 5)
    success_probability = np.clip(baseline + treatment * uplift, 0.03, 0.80)
    meaningful_task = rng.binomial(1, success_probability)
    error_probability = np.clip(0.012 + 0.007 * treatment + 0.004 * (device == "Mobile"), 0, 1)
    serious_error = rng.binomial(1, error_probability)
    experiment = pd.DataFrame(
        {
            "account_id": [f"A{index:05d}" for index in range(1, n_experiment + 1)],
            "treatment": treatment,
            "device": device,
            "region": exp_region,
            "prior_tasks_30d": prior_tasks,
            "meaningful_task_7d": meaningful_task,
            "serious_error_7d": serious_error,
        }
    )
    experiment_folder = data_path("synthetic_product_experiment")
    experiment_folder.mkdir(parents=True, exist_ok=True)
    experiment.to_csv(experiment_folder / "product_experiment.csv", index=False)
    experiment_metadata = {
        "title": "Synthetic product experiment",
        "generator": "scripts/generate_synthetic.py",
        "seed": SEED,
        "rows": len(experiment),
        "real_people": False,
        "assignment": "exactly 4,000 accounts per arm, randomly permuted",
        "designed_effect": "positive average task-completion effect with device heterogeneity",
        "guardrail": "treatment increases serious-error probability",
    }
    (experiment_folder / "metadata.json").write_text(
        json.dumps(experiment_metadata, indent=2), encoding="utf-8"
    )
    print(f"wrote {len(experiment):,} rows to {experiment_folder / 'product_experiment.csv'}")


if __name__ == "__main__":
    main()
