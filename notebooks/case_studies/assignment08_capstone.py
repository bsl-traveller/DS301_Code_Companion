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
# # Assignment 8 — End-to-end decision project
# Select one catalog dataset or the synthetic customer-operations dataset. The project is evaluated as a chain from decision to monitored action, not as a contest for the highest model score.

# %%
import pandas as pd

from ds301.paths import data_path

# Replace with the dataset selected in your approved project charter.
path = data_path("synthetic_customer_operations/customer_operations.csv")
data = pd.read_csv(path)
data.head()

# %% [markdown]
# ## Required project record
# 1. Decision charter: owner, population, action, outcome, guardrails and non-goals.
# 2. Source contract: grain, time, coverage, lineage, permission and limitations.
# 3. Reproducible preparation with reconciliation checks.
# 4. EDA with distributions, comparisons, time and relationships.
# 5. Baseline and, only if useful, one additional analytical method.
# 6. Technical, decision and responsible evaluation.
# 7. Three-to-five-view explanatory story.
# 8. Pilot, monitoring, fallback and learning plan.

# %%
# Build your reproducible project below. Use markdown cells to preserve reasoning.

# %% [markdown]
# Reference structure: `solutions/assignment08_capstone_solution.py`.
