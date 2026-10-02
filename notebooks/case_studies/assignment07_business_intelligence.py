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
# # Assignment 7 — Business intelligence with public indicators
# **Decision:** what can a small indicator dashboard support—and what can it not establish?
#
# Source: World Bank Indicators API v2. No API key is required.

# %%
import pandas as pd

from ds301 import load_dataset
from ds301.paths import data_path

path = data_path("open/world_bank_india/data.csv")
if not path.exists():
    load_dataset("world_bank_india")
data = pd.read_csv(path)
data.head()

# %% [markdown]
# ## Tasks
# 1. Create a metric contract for every indicator: definition, unit, source, frequency and caveat.
# 2. Reshape long data to a year-by-indicator table without inventing missing observations.
# 3. Design an overview, trend view and metadata/quality view.
# 4. Annotate missing years and distinguish percent, percentage-point and growth-rate changes.
# 5. Write three supported findings and three claims that the dashboard cannot support.

# %%
# Begin your dashboard analysis here.

# %% [markdown]
# Use the decision question, stated data limitations, and reusable helpers in `src/ds301/` to guide your implementation.
