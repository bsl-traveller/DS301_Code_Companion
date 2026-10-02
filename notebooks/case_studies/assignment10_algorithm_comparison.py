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
# # Assignment 10 — Algorithm comparison at operating capacity
# **Decision:** which eligible records should enter a limited follow-up queue?
#
# Source: UCI Bank Marketing, DOI 10.24432/C5K306, CC BY 4.0. Observed
# subscription is not the causal effect of contact.

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
# 1. Define prediction origin and remove `duration`, which is known only after contact.
# 2. Build identical preprocessing for a logistic baseline and a tree ensemble.
# 3. Compare ROC AUC, Brier score, calibration, and precision/lift at 5%, 10%,
#    and 20% review capacity.
# 4. Use repeated or future-like validation and report uncertainty/stability.
# 5. Compare latency, explanation burden, failure modes, and maintenance—not
#    only predictive rank.

# %%
# Begin your algorithm-comparison workflow here.

# %% [markdown]
# Use the decision question, stated data limitations, and reusable helpers in `src/ds301/` to guide your implementation.
