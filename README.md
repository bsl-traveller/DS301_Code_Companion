# DS301: Data Science — course companion

This is the programming companion for **DS301: Data Science: An Introduction**. Use it alongside the lectures to explore concepts, practise with case studies, and complete assignments.

## Repository layout

- `notebooks/01_*` through `notebooks/10_*` — the lecture notebooks, in teaching order. See `LECTURE_COVERAGE.md` before class.
- `notebooks/case_studies/` — ten case studies for guided practice. Each has a classroom-ready `.ipynb` notebook and matching `.py` source.
- `notebooks/solutions/` — instructor/reference solutions paired with the case studies. Use these only after attempting the corresponding case.
- `assignments/` — five briefs aligned to the first ten lectures.
- `src/ds301/` — reusable utilities that help notebooks locate, validate, and load datasets.
- `data/` — where generated and downloaded datasets are stored on your computer.
- `docs/data/` — data definitions, sources, and guidance for appropriate use.
- `outputs/` — created locally when you save charts, tables, or reports while exploring; it is safe to delete and is not needed to run the course notebooks.
- `scripts/` — explicit commands for downloading open data and generating synthetic teaching data.
- `tests/` — automated checks used to keep the supporting utilities reliable.

## Start here

Read [SETUP.md](SETUP.md) to install the course environment. Then work through the numbered lecture notebooks in order, attempt the matching case study, and consult the corresponding reference solution only after making your own attempt. Before using a case-study dataset, read [the dataset manifest](docs/data/DATASET_MANIFEST.md) for its source and limitations.

## Working with notebooks

Use Python 3.14.x and open the `.ipynb` files in JupyterLab. Run cells in order; pause at the reflection prompts and adapt the examples to test your understanding. The supporting `ds301` package handles dataset locations and checks dataset descriptions before data is downloaded or saved.
