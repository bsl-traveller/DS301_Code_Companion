"""Path helpers that make notebooks work from Jupyter's nested directories."""

from __future__ import annotations

import os
from pathlib import Path


def project_root(start: Path | None = None) -> Path:
    """Return the repository root without relying on an OS-specific path.

    The resolver first honours ``DS301_PROJECT_ROOT`` for unusual launches,
    then searches from the caller/current directory and finally from this
    installed package's source location. The latter supports editable Poetry
    installs when Jupyter was started outside the repository.
    """
    configured_root = os.environ.get("DS301_PROJECT_ROOT")
    anchors = [Path(configured_root)] if configured_root else []
    anchors.extend([start or Path.cwd(), Path(__file__).resolve()])
    for anchor in anchors:
        resolved = anchor.resolve()
        candidates = (resolved, *resolved.parents) if resolved.is_dir() else resolved.parents
        for candidate in candidates:
            if (candidate / "pyproject.toml").is_file() and (candidate / "data").is_dir():
                return candidate
    raise RuntimeError(
        "Could not find the DS301 repository. Start Jupyter from the cloned repository "
        "or set DS301_PROJECT_ROOT to that folder."
    )


def data_path(relative_path: str) -> Path:
    """Return a safe path below the repository's local ``data/`` directory."""
    relative = Path(relative_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("relative_path must stay inside data/")
    return project_root() / "data" / relative
