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
# # Assignment 2 — Time-series reasoning with UCI Bike Sharing
# **Decision:** how should an operator plan capacity for the next comparable period?
#
# Source: Fanaee-T (2013), UCI Bike Sharing, DOI 10.24432/C5W894, CC BY 4.0.

# %%
import pandas as pd

from ds301 import load_dataset
from ds301.paths import data_path

path = data_path("open/bike_sharing/data.csv")
if not path.exists():
    load_dataset("bike_sharing")
data = pd.read_csv(path)
data.head()

# %% [markdown]
# ## Tasks
# 1. Identify time grain, target, weather/calendar variables and variables unavailable at forecast origin.
# 2. Plot demand by date and seasonal group; show missing periods explicitly.
# 3. Compare naive and seasonal-naive forecasts using MAE and signed bias.
# 4. Use a chronological holdout; explain why a random split is inappropriate.
# 5. Translate uncertainty into a capacity decision and two guardrails.

# %%
# Begin your analysis here.

# %% [markdown]
# Use the decision question, stated data limitations, and reusable helpers in `src/ds301/` to guide your implementation.
