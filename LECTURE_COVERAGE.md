# Notebook guide: Lectures 1–10

The notebooks are designed to be read, run, discussed, and adapted in class. Each uses a small business case, explains the concept in plain language, and makes the reasoning visible with charts or diagrams.

| Lecture | Core ideas explored visually | Practice outcome |
| --- | --- | --- |
| 1. Decision to evidence | evidence-to-action loop; comparison and guardrails; the overlap of statistics, analytics, ML, and AI; four ingredients of useful data science; responsible-use gates | Frame a recurring decision with an outcome, comparison, limitation, and guardrail. |
| 2. Problem framing | descriptive, diagnostic, predictive, and prescriptive lenses; association versus common cause; decision canvas; metric/KPI/decision-rule chain; leading and lagging evidence; feasibility | Turn a vague concern into an action-ready analytical question. |
| 3. Lifecycle | CRISP-DM loop; stage artefacts; OSEMN mapping; technical versus business success; learning loops | Design the evidence and monitoring needed around a model. |
| 4. Ecosystem | ownership network; hand-off acceptance rates and delays; RACI view; data journey; capability-to-tool mapping | Assign accountable roles, acceptance rules, and proportionate tools. |
| 5. Business data | data forms; field dictionary; grain and keys; one-to-many join effect; availability and leakage; source fitness; data audit; proportional collection | Choose and audit sources that fit a decision and time boundary. |
| 6. Time series | trend, seasonality, aggregation, moving averages, ETS/Holt/seasonal ETS, lags, ACF/PACF, ARIMA, chronological and rolling validation, forecast errors, anomalies | Produce and assess forecasts without leaking future information. |
| 7. ML fundamentals | learning settings; absolute, squared, Huber, and log loss; empirical risk; loss surface and gradient-descent path; batch/stochastic updates; complexity, regularisation, leakage, cross-validation, ROC/PR/calibration | Explain why a model is selected and how it is validated. |
| 8. Regression | conditional mean equation; residuals; MSE/MAE loss surfaces; multiple regression; interactions; leverage and influence; collinearity; model comparison; ridge and tree alternatives | Build, diagnose, and communicate a regression model with its limitations. |
| 9. Classification | sigmoid and log odds; log loss; logistic boundaries; threshold trade-offs; confusion matrix; ROC, precision–recall, calibration; k-NN, Naive Bayes, and SVM boundaries; cost-sensitive action | Turn a predicted probability into a defensible, monitored decision rule. |
| 10. Ensembles and unsupervised learning | impurity and tree partitions; depth; bootstrap samples; ensemble correlation; random forest, out-of-bag assessment, boosting, importance; k-means updates, silhouette, hierarchical/DBSCAN patterns, PCA projection | Compare model structure, stability, and useful unsupervised summaries. |

As you work through a notebook, pause at each visual and answer four questions: What does it show? What comparison makes it meaningful? What does it not establish? What action, if any, could follow responsibly?

## Worked datasets and three-dimensional loss

Lectures 1–5 each include the complete Wine Recognition exercise: inspect raw rows and feature ranges, reserve test records, fit a majority baseline, tune a scaled logistic pipeline inside training folds, inspect a held-out confusion matrix, and write the decision statement. Each lecture poses its own framing, lifecycle, ownership or data-quality questions about those results.

Lectures 7–8 connect raw wine measurements to a table of residuals, a 3D MSE landscape, its contour projection, gradient-descent updates, and the corresponding regression equations. Separate MSE, MAE and Huber surfaces show how changing the objective changes both geometry and the fitted line. A learning-rate comparison and Hessian condition numbers explain optimisation stability. Lecture 9 adds a 3D binary log-loss surface.

Lecture 7 also includes learning curves on observed wine data, nested model selection with a final held-out test, a controlled bias–variance experiment, mini-batch and momentum comparisons, and explicitly simulated distribution shifts. The simulations make quantities visible that cannot be directly recovered from a single observed dataset.
