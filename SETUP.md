# Student setup guide

These steps work on Windows, macOS, and Linux. Commands use Poetry, so you do not need to activate a virtual environment manually.

## 1. Install prerequisites

Install Python **3.14.x**. During Python installation on Windows, select **Add Python to PATH**. Confirm Python is available:

```bash
python --version
```

On Windows, `py -3.14 --version` is often the most reliable Python check. On macOS and Linux, use `python3.14 --version` if `python` points to another version.

### Install Poetry

Use Poetry's official installer; it installs Poetry separately from the course environment.

**Windows PowerShell**

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

Close and reopen PowerShell, then verify:

```powershell
poetry --version
```

If `poetry` is not recognized, follow the installer's PATH message, then reopen the terminal. The usual location is `%APPDATA%\Python\Scripts`.

**macOS or Linux**

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Close and reopen the terminal, then verify:

```bash
poetry --version
```

If the command is not found, add Poetry's bin directory to your shell PATH as instructed by the installer (commonly `$HOME/.local/bin`), reopen the terminal, and run the verification again. See [Poetry's installation documentation](https://python-poetry.org/docs/#installation) for a managed or proxy-restricted computer.

## 2. Create the course environment

From the `DS301_Code_Companion` folder you downloaded, run:

```bash
poetry env use 3.14
poetry install
```

Poetry creates the local `.venv` automatically.

On Windows, if `poetry env use 3.14` cannot find Python, provide the launcher instead:

```powershell
$python = py -3.14 -c "import sys; print(sys.executable)"
poetry env use $python
poetry install
```

On macOS or Linux, use the full interpreter command when needed:

```bash
poetry env use python3.14
poetry install
```

## 3. Prepare local data

Datasets are prepared on your computer so the notebooks remain lightweight. Generate the synthetic datasets once:

```bash
poetry run python scripts/generate_synthetic.py
```

Download an open dataset when a case study needs it:

```bash
poetry run python scripts/download_open_data.py --dataset bike_sharing
```

To download the full catalogue, use `--all`. Read [the dataset manifest](docs/data/DATASET_MANIFEST.md) first so you understand each dataset's source and limitations.

## 4. Open notebooks

From the repository root, start JupyterLab:

```bash
poetry run jupyter lab
```

Open a lecture notebook in `notebooks/`, then use `notebooks/case_studies/` for practice. Reference solutions are in `notebooks/solutions/`.

Keep JupyterLab open at the course folder and run notebook cells in order. The supplied notebooks and scripts work on Windows, macOS, and Linux.

## 5. Verify your installation

```bash
poetry run python -c "import ds301; print('DS301 is ready')"
```

If you see `DS301 is ready`, open JupyterLab and begin with the first lecture notebook.
