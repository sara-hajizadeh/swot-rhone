"""Look at the quality fields of the clean reach table before choosing QC thresholds."""

import pandas as pd

df = pd.read_parquet("data/interim/reach_clean.parquet")
print(len(df), "observations")

for col in ["reach_q", "xovr_cal_q", "ice_clim_f", "partial_f"]:
    print(f"\n{col}:")
    print(df[col].value_counts(dropna=False).sort_index())

print("\ndark_frac:")
print(df["dark_frac"].describe())

print("\nwse_u (m):")
print(df["wse_u"].describe())