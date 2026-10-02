# Case studies

Each case study has a classroom notebook (`.ipynb`) and matching Python source (`.py`). Work in the notebook unless your instructor asks you to use the source file.

| Case study | Decision context | Dataset | Lecture connection |
| --- | --- | --- | --- |
| 01 Quality audit | Can service data support a regional review? | Synthetic operations | 5 |
| 02 Forecasting | How should capacity be planned? | UCI Bike Sharing | 6 |
| 03 Retail EDA | Which patterns deserve investigation? | UCI Online Retail | 5 |
| 04 Classification | Which records should receive follow-up? | UCI Bank Marketing | 9 |
| 05 Segmentation | Can spending summaries guide service? | UCI Wholesale Customers | 10 |
| 06 Responsible audit | What do subgroup errors reveal? | UCI Adult | 7–9 |
| 07 Public indicators | What can a dashboard support? | World Bank API | 1–5 |
| 08 Capstone | How does a decision-to-evidence project fit together? | Student-selected | 1–10 |
| 09 Bootstrap evidence | Is a regional difference sufficiently stable? | Synthetic operations | 7 |
| 10 Model comparison | Which model suits a limited queue? | UCI Bank Marketing | 7–10 |

To prepare data, run `poetry run python scripts/download_open_data.py --dataset bike_sharing` or `poetry run python scripts/generate_synthetic.py`. Consult [the dataset manifest](../../docs/data/DATASET_MANIFEST.md) before using an open dataset.
