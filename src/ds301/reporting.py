"""Small reusable checks for the companion notebooks."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .paths import project_root


def ensure_output(name: str) -> Path:
    """Create and return a repository-rooted ignored output directory."""
    folder = project_root() / "outputs" / name
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def audit_table(data: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "dtype": data.dtypes.astype(str),
            "missing_n": data.isna().sum(),
            "missing_pct": data.isna().mean().mul(100).round(2),
            "unique_n": data.nunique(dropna=True),
        }
    )


def save_figure(path: Path) -> None:
    plt.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches="tight")
    plt.close()
