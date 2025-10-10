from __future__ import annotations
import pandas as pd
from pathlib import Path
from src.utils.io import read_csv_smart

# Gera dataframe consolidado p/ UI

def load_market_history(path: Path) -> pd.DataFrame:
    df = read_csv_smart(path)
    if df.empty:
        return df
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    df = df.sort_values("ts")
    return df