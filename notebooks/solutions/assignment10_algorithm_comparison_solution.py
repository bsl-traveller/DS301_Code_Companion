"""Reference solution: compare models at realistic review capacities."""

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from ds301 import load_dataset
from ds301.paths import data_path
from ds301.reporting import ensure_output

path = data_path("open/bank_marketing/data.csv")
if not path.exists():
    load_dataset("bank_marketing")
data = pd.read_csv(path)
y = data.pop("y").eq("yes").astype(int)
data = data.drop(columns=["duration"])
numeric = data.select_dtypes(include="number").columns.tolist()
categorical = [column for column in data.columns if column not in numeric]
preprocess = ColumnTransformer(
    [
        (
            "num",
            Pipeline(
                [
                    ("impute", SimpleImputer(strategy="median")),
                    ("scale", StandardScaler()),
                ]
            ),
            numeric,
        ),
        (
            "cat",
            Pipeline(
                [
                    ("impute", SimpleImputer(strategy="most_frequent")),
                    ("encode", OneHotEncoder(handle_unknown="ignore")),
                ]
            ),
            categorical,
        ),
    ]
)
x_train, x_test, y_train, y_test = train_test_split(
    data,
    y,
    test_size=0.3,
    random_state=301,
    stratify=y,
)
models = {
    "logistic": LogisticRegression(max_iter=1_500),
    "random_forest": RandomForestClassifier(
        n_estimators=300,
        min_samples_leaf=20,
        random_state=301,
        n_jobs=-1,
    ),
}


def capacity_metrics(y_true: pd.Series, score: pd.Series, share: float) -> dict[str, float]:
    """Calculate queue precision, recall, and lift at a fixed capacity share."""
    count = max(1, round(len(score) * share))
    selected = score.nlargest(count).index
    positives = y_true.loc[selected].sum()
    precision = positives / count
    recall = positives / y_true.sum()
    return {
        "capacity": share,
        "precision": precision,
        "recall": recall,
        "lift": precision / y_true.mean(),
    }


rows: list[dict[str, float | str]] = []
for name, estimator in models.items():
    pipeline = Pipeline([("prepare", preprocess), ("model", estimator)])
    pipeline.fit(x_train, y_train)
    probability = pd.Series(pipeline.predict_proba(x_test)[:, 1], index=y_test.index)
    common = {
        "model": name,
        "roc_auc": roc_auc_score(y_test, probability),
        "brier": brier_score_loss(y_test, probability),
    }
    for capacity in (0.05, 0.10, 0.20):
        rows.append(common | capacity_metrics(y_test, probability, capacity))

results = pd.DataFrame(rows)
output = ensure_output("assignment10_algorithm_comparison")
results.to_csv(output / "capacity_metrics.csv", index=False)
print(results.to_string(index=False))
print("Association under historical contact policy is not incremental treatment effect.")
