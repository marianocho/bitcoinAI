from __future__ import annotations
from pathlib import Path
import pandas as pd


def read_csv_smart(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def append_csv(path: Path, df: pd.DataFrame) -> None:
    header = not path.exists()
    df.to_csv(path, mode="a", header=header, index=False)