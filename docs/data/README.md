# Data guide

Use these guides before working with a dataset in a case study or assignment.

- `DATA_DICTIONARY.md` describes the small classroom datasets used in the lecture notebooks.
- `DATASET_MANIFEST.md` records the source, licence context, teaching purpose, and cautions for case-study datasets.

## Where datasets are stored

```text
data/                              # created locally; not included in the course repository
├── open/<dataset>/data.csv          # created by scripts/download_open_data.py
├── synthetic_customer_operations/  # created by scripts/generate_synthetic.py
├── synthetic_subscription_duration/
└── synthetic_product_experiment/
```

The download and generation commands in [SETUP.md](../../SETUP.md) place data here automatically.
