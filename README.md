# DS301: Data Science — course companion

This repository is the programming companion for the material delivered in **DS301: Data Science: An Introduction**. It intentionally separates classroom concept notebooks from executable examples that address a concrete decision using real or explicitly synthetic datasets.

## Repository layout

- `lectures/` — one self-contained notebook for each delivered lecture (Lectures 1–10), organised in teaching order. `lectures/README.md` records the concept and practice outcome for each session.
- `assignments/` — the five assignment briefs aligned to the first ten lectures.
- `real-world-examples/` — runnable, Jupytext-paired examples for Projects 1–10. Each project is a distinct decision problem, with source code, a notebook rendering, data-acquisition scripts, provenance metadata, and lightweight reusable helpers.

## Branch policy

`main` is reserved for the small, stable repository foundation. Teaching material belongs on `course/content`, and should be committed incrementally as it is covered in class. This checkout is on `course/content`; no files have been committed or staged by the setup.

## Data policy

The repository contains code, notebooks, assignment briefs, and dataset metadata only. Raw data, synthetic generated data, notebook checkpoints, environments, caches, and generated outputs are ignored. For real-world examples, follow `real-world-examples/data/DATASET_MANIFEST.md` and run the relevant command in `real-world-examples/scripts/` to create the local data copy. Do not commit those files.

## Working with notebooks

The Python files in `real-world-examples/notebooks/` are the version-control-friendly notebook sources. Their paired `.ipynb` files are included for direct classroom use. Regenerate a notebook locally, if needed, with Jupytext:

```bash
cd real-world-examples
poetry install
poetry run jupytext --to ipynb notebooks/assignment01_quality_audit.py
```

The lecture notebooks use the dependencies declared in `pyproject.toml` at the repository root.
