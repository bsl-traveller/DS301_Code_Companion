"""Download the book companion's open datasets with source metadata."""

from __future__ import annotations

import argparse
from pathlib import Path

from ds301 import DATASETS, load_dataset
from ds301.paths import data_path


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dataset", choices=sorted(DATASETS))
    group.add_argument("--all", action="store_true")
    parser.add_argument(
        "--output",
        help="Optional local destination; defaults to the repository's data/open directory.",
    )
    args = parser.parse_args()

    keys = sorted(DATASETS) if args.all else [args.dataset]
    for key in keys:
        output_root = Path(args.output) if args.output else data_path("open")
        frame = load_dataset(key, output_root)
        print(f"{key}: {len(frame):,} rows x {frame.shape[1]} columns")


if __name__ == "__main__":
    main()
