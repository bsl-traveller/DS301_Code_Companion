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
# # Assignment 4 — Classification as a decision system
# **Decision:** which records, if any, should be prioritised for a costly follow-up?
#
# Source: Moro, Rita & Cortez (2014), UCI Bank Marketing, DOI 10.24432/C5K306, CC BY 4.0.

# %%
import pandas as pd

from ds301 import load_dataset
from ds301.paths import data_path

path = data_path("open/bank_marketing/data.csv")
if not path.exists():
    load_dataset("bank_marketing")
data = pd.read_csv(path)
data.head()

# %% [markdown]
# ## Tasks
# 1. Define target, prevalence, decision moment and a naive baseline.
# 2. Exclude fields unavailable at the pre-contact decision moment; explain `duration` leakage.
# 3. Build a train/test preprocessing pipeline and logistic-regression baseline.
# 4. Report confusion matrix, precision, recall, ROC AUC and a capacity-based top-k analysis.
# 5. Distinguish predicted subscription from incremental campaign effect.

# %%
# Begin your model here.

# %% [markdown]
# Use the decision question, stated data limitations, and reusable helpers in `src/ds301/` to guide your implementation.
