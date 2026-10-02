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
# # Assignment 6 — Responsible-AI audit
# This exercise uses the historical UCI Adult dataset to examine measurement and error disparities—not to endorse income prediction as a legitimate decision use.
#
# Source: Becker & Kohavi (1996), UCI Adult, DOI 10.24432/C5XW20, CC BY 4.0.

# %%
import pandas as pd

from ds301 import load_dataset
from ds301.paths import data_path

path = data_path("open/adult/data.csv")
if not path.exists():
    load_dataset("adult")
data = pd.read_csv(path)
data.head()

# %% [markdown]
# ## Tasks
# 1. Audit the target, 1994 observation context, category construction, missingness and sample selection.
# 2. Write an impact statement defining a hypothetical low-consequence educational use—or reject the proposed use.
# 3. Fit a transparent baseline only for audit demonstration.
# 4. Report base rates and false-positive/false-negative rates with denominators by group.
# 5. Explain why metric parity cannot establish fairness or legitimate purpose.

# %%
# Begin your critical audit here.

# %% [markdown]
# Use the decision question, stated data limitations, and reusable helpers in `src/ds301/` to guide your implementation.
