# ---
# kernelspec:
#   display_name: Python 3
#   language: python
#   name: python3
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
# ---

# %% [markdown]
# # Assignment 9 — Statistical inference and bootstrap
# **Decision:** is a regional difference in delivery time large and stable enough
# to justify a process investigation?
#
# The dataset is explicitly synthetic. It represents no real customer or firm.

# %%
import pandas as pd

from ds301.paths import data_path

path = data_path("synthetic_customer_operations/customer_operations.csv")
data = pd.read_csv(path)
data[["region", "delivery_minutes", "returned"]].head()

# %% [markdown]
# ## Tasks
# 1. Define the estimator and the population/process to which it refers.
# 2. Compare region means, medians, quantiles, counts, and tail probabilities.
# 3. Construct a fixed-seed cluster-aware or row bootstrap appropriate to the
#    unit of observation; explain the exchangeability assumption.
# 4. Estimate an interval for a chosen regional mean difference and perform a
#    sensitivity analysis using a trimmed mean or median.
# 5. Translate the uncertainty into a proportionate investigation decision;
#    do not treat an interval as proof of a causal regional effect.

# %%
# Begin your inference workflow here.

# %% [markdown]
# Use the decision question, stated data limitations, and reusable helpers in `src/ds301/` to guide your implementation.
