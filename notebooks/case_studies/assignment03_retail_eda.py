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
# # Assignment 3 — Transactional EDA and customer analytics
# **Decision:** which customer or transaction patterns deserve investigation before a retention action?
#
# Source: Chen (2015), UCI Online Retail, DOI 10.24432/C5BW33, CC BY 4.0.

# %%
import pandas as pd

from ds301 import load_dataset
from ds301.paths import data_path

path = data_path("open/online_retail/data.csv")
if not path.exists():
    load_dataset("online_retail")
data = pd.read_csv(path)
data.head()

# %% [markdown]
# ## Tasks
# 1. Define the row grain and distinguish cancellation lines from positive sales.
# 2. Reconcile line, invoice and customer counts. Assess missing identifiers.
# 3. Plot monthly observed sales, order-value distribution and cancellations by country.
# 4. Construct recency, frequency and monetary summaries with an explicit snapshot date.
# 5. Propose a testable retention action; explain why high historical value alone does not estimate treatment response.

# %%
# Begin your analysis here.

# %% [markdown]
# Use the decision question, stated data limitations, and reusable helpers in `src/ds301/` to guide your implementation.
