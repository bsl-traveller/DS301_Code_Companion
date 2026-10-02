"""Reference solution: critical subgroup audit using the UCI Adult dataset."""

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from ds301 import load_dataset
from ds301.paths import data_path
from ds301.reporting import ensure_output

path = data_path("open/adult/data.csv")
if not path.exists():
    load_dataset("adult")
data = pd.read_csv(path).replace("?", np.nan)
target = next(c for c in data if "income" in c.lower())
y = data[target].astype(str).str.contains(">50K", regex=False).astype(int)
protected_for_audit = "sex"
X = data.drop(columns=[target])
cat = X.select_dtypes(exclude="number").columns
num = X.select_dtypes(include="number").columns
prepare = ColumnTransformer(
    [
        ("num", Pipeline([("i", SimpleImputer(strategy="median")), ("s", StandardScaler())]), num),
        (
            "cat",
            Pipeline(
                [
                    ("i", SimpleImputer(strategy="most_frequent")),
                    ("o", OneHotEncoder(handle_unknown="ignore")),
                ]
            ),
            cat,
        ),
    ]
)
model = Pipeline([("prepare", prepare), ("model", LogisticRegression(max_iter=1000))])
train, test = train_test_split(data.index, test_size=0.3, random_state=301, stratify=y)
model.fit(X.loc[train], y.loc[train])
pred = model.predict(X.loc[test])

rows = []
for group, idx in X.loc[test].groupby(protected_for_audit).groups.items():
    tn, fp, fn, tp = confusion_matrix(
        y.loc[idx], pred[test.get_indexer(idx)], labels=[0, 1]
    ).ravel()
    rows.append({"group": group, "n": len(idx), "FPR": fp / (fp + tn), "FNR": fn / (fn + tp)})
audit = pd.DataFrame(rows)
audit.to_csv(ensure_output("assignment06_responsible_ai") / "subgroup_error_audit.csv", index=False)
print(audit)
print(
    "Interpretation warning: metric differences require context; parity alone is not responsible use."
)
