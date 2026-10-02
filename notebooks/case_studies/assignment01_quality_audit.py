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
# # Assignment 1 — Data contract and quality audit
# **Decision:** can the synthetic customer-operations table support a regional service review?
#
# Before changing data, state the unit, population, period, important fields and five invariants.

# %%
import pandas as pd

from ds301.paths import data_path

path = data_path("synthetic_customer_operations/customer_operations.csv")
if not path.exists():
    raise FileNotFoundError("Run: poetry run python scripts/generate_synthetic.py")
data = pd.read_csv(path, parse_dates=["order_date"])
data.head()

# %% [markdown]
# ## Tasks
# 1. Profile types, missingness, unique counts and ranges.
# 2. Identify duplicated order identifiers and reconcile order value before/after treatment.
# 3. Test whether satisfaction missingness differs by return status, region and month.
# 4. Produce one distribution, one group comparison and one time plot.
# 5. Write a 250-word data-quality decision note. Do not impute satisfaction without a use-specific argument.

# %%
# Begin your audit here.

# %% [markdown]
# Use the decision question, stated data limitations, and reusable helpers in `src/ds301/` to guide your implementation.
