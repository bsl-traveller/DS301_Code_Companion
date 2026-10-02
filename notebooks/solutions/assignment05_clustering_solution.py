"""Reference solution: UCI Wholesale Customers clustering."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from ds301 import load_dataset
from ds301.paths import data_path
from ds301.reporting import ensure_output, save_figure

path = data_path("open/wholesale_customers/data.csv")
if not path.exists():
    load_dataset("wholesale_customers")
data = pd.read_csv(path)
spend = data.select_dtypes(include="number").drop(columns=["Channel", "Region"], errors="ignore")
Z = StandardScaler().fit_transform(np.log1p(spend))
scores = {}
for k in range(2, 7):
    labels = KMeans(n_clusters=k, n_init=20, random_state=301).fit_predict(Z)
    scores[k] = silhouette_score(Z, labels)
best_k = max(scores, key=scores.get)
labels = KMeans(n_clusters=best_k, n_init=30, random_state=301).fit_predict(Z)
profiles = data.assign(cluster=labels).groupby("cluster")[spend.columns].median()
profiles.to_csv(ensure_output("assignment05_clustering") / "cluster_profiles.csv")
plt.plot(list(scores), list(scores.values()), marker="o", color="#006D77")
plt.xlabel("Number of clusters")
plt.ylabel("Silhouette score")
plt.title("UCI Wholesale Customers: diagnostic, not proof of natural segments")
save_figure(ensure_output("assignment05_clustering") / "silhouette.png")
