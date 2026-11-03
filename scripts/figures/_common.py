"""Shared paths for the figure scripts.

Every figure script reads only files in this repository. By default it writes its
PNG to Figures/images/; pass a directory as the first argument to write there instead.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "Data"
PLOT_DATA = REPO / "Figures/plot_data"


def out_path(name: str) -> Path:
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "Figures/images"
    folder.mkdir(parents=True, exist_ok=True)
    return folder / name


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))
