"""Rank overpasses by how much of the main channel they see after QC."""

import pandas as pd

qc = pd.read_parquet("data/processed/reach_qc.parquet")
kept = qc[qc["qc_pass"]]

by_pass = kept.groupby(["cycle", "pass_id"]).agg(
    date=("datetime", "min"),
    n_reaches=("reach_id", "nunique"),
    dark=("dark_frac", "median"),
)
by_pass = by_pass.sort_values(["n_reaches", "dark"], ascending=[False, True])
print(by_pass.head(10))