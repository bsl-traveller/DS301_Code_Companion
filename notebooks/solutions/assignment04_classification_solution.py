"""Reference solution: Bank Marketing classification and decision evaluation."""

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_recall_curve,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from ds301 import load_dataset
from ds301.paths import data_path
from ds301.reporting import ensure_output, save_figure

path = data_path("open/bank_marketing/data.csv")
if not path.exists():
    load_dataset("bank_marketing")
data = pd.read_csv(path)
target = "y"
y = data[target].astype(str).str.lower().str.strip().map({"yes": 1, "no": 0})
# Duration is known only after the call and is excluded for pre-call targeting.
X = data.drop(columns=[target, "duration"], errors="ignore")
categorical = X.select_dtypes(exclude="number").columns
numeric = X.select_dtypes(include="number").columns
preprocess = ColumnTransformer(
    [
        (
            "num",
            Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]),
            numeric,
        ),
        (
            "cat",
            Pipeline(
                [
                    ("impute", SimpleImputer(strategy="most_frequent")),
                    ("onehot", OneHotEncoder(handle_unknown="ignore")),
                ]
            ),
            categorical,
        ),
    ]
)
model = Pipeline([("prepare", preprocess), ("model", LogisticRegression(max_iter=1000))])
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=301, stratify=y
)
model.fit(X_train, y_train)
probability = model.predict_proba(X_test)[:, 1]
prediction = (probability >= 0.5).astype(int)
prevalence = y_test.mean()
print("positive prevalence", prevalence)
print("always-negative accuracy", 1 - prevalence)
print("ROC AUC", roc_auc_score(y_test, probability))
print(classification_report(y_test, prediction))
output = ensure_output("assignment04_classification")
confusion = pd.DataFrame(
    confusion_matrix(y_test, prediction),
    index=["actual_no", "actual_yes"],
    columns=["predicted_no", "predicted_yes"],
)
confusion.to_csv(output / "confusion_matrix.csv")

# Evaluate the ranking at the call centre's actual capacity rather than at an arbitrary .5 cutoff.
capacity_share = 0.10
ranking = pd.DataFrame({"actual": y_test.to_numpy(), "probability": probability}).sort_values(
    "probability", ascending=False
)
capacity = max(1, round(len(ranking) * capacity_share))
selected = ranking.head(capacity)
true_positives = int(selected["actual"].sum())
precision_at_capacity = true_positives / capacity
recall_at_capacity = true_positives / int(ranking["actual"].sum())
lift_at_capacity = precision_at_capacity / prevalence
assumed_value_per_subscription = 3000
assumed_cost_per_call = 120
illustrative_value = (
    assumed_value_per_subscription * true_positives - assumed_cost_per_call * capacity
)
capacity_result = pd.DataFrame(
    [
        {
            "test_records": len(ranking),
            "capacity_share": capacity_share,
            "actions": capacity,
            "true_positives": true_positives,
            "precision_at_capacity": precision_at_capacity,
            "recall_at_capacity": recall_at_capacity,
            "lift_at_capacity": lift_at_capacity,
            "illustrative_value": illustrative_value,
        }
    ]
)
capacity_result.to_csv(output / "capacity_evaluation.csv", index=False)
print(capacity_result.to_string(index=False))

fpr, tpr, _ = roc_curve(y_test, probability)
precision_curve, recall_curve, _ = precision_recall_curve(y_test, probability)
figure, axes = plt.subplots(1, 2, figsize=(10, 4.3))
axes[0].plot(fpr, tpr, color="#006D77", linewidth=2)
axes[0].plot([0, 1], [0, 1], color="#5D6870", linestyle="--")
axes[0].set(xlabel="False-positive rate", ylabel="True-positive rate", title="ROC curve")
axes[1].plot(recall_curve, precision_curve, color="#E29520", linewidth=2)
axes[1].axhline(prevalence, color="#5D6870", linestyle="--", label="prevalence")
axes[1].set(xlabel="Recall", ylabel="Precision", title="Precision--recall curve")
axes[1].legend()
save_figure(output / "ranking_curves.png")

print(
    "Decision interpretation: the value calculation is illustrative and assumes every observed "
    "positive in the selected group was created by a call. The historical labels support response "
    "ranking, not incremental treatment effect; a campaign pilot needs randomised no-contact "
    "evidence, contact eligibility, opt-out and burden guardrails."
)
