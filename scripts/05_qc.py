"""Apply flag-based quality control and report how much data each test removes."""

from pathlib import Path

import pandas as pd
import yaml

from swot_rhone.qc import flag_checks, qc_summary

with open("config/rhone.yaml") as f:
    cfg = yaml.safe_load(f)

df = pd.read_parquet("data/interim/reach_clean.parquet")
checks = flag_checks(df, cfg["qc"])
summary = qc_summary(checks)
print(summary)

df["qc_pass"] = ~checks.any(axis=1)

Path("data/processed").mkdir(parents=True, exist_ok=True)
df.to_parquet("data/processed/reach_qc.parquet")

Path("output/tables").mkdir(parents=True, exist_ok=True)
summary.to_csv("output/tables/qc_summary.csv")