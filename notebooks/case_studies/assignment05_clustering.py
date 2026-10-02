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
# # Assignment 5 — Clustering and segment interpretation
# **Decision:** can spending-pattern summaries support differentiated account service?
#
# Source: Cardoso (2013), UCI Wholesale Customers, DOI 10.24432/C5030X, CC BY 4.0.

# %%
import pandas as pd

from ds301 import load_dataset
from ds301.paths import data_path

path = data_path("open/wholesale_customers/data.csv")
if not path.exists():
    load_dataset("wholesale_customers")
data = pd.read_csv(path)
data.head()

# %% [markdown]
# ## Tasks
# 1. Plot spending distributions and justify log transformation and scaling.
# 2. Compare several cluster counts using silhouette score and stability under seed changes.
# 3. Profile medians and within-cluster dispersion in original units.
# 4. Compare clusters with channel/region only after fitting; avoid circular interpretation.
# 5. State what evidence is still required before changing customer treatment.

# %%
# Begin your clustering analysis here.

# %% [markdown]
# Use the decision question, stated data limitations, and reusable helpers in `src/ds301/` to guide your implementation.
