"""Make the project figures."""

from pathlib import Path

import geopandas as gpd
import pandas as pd

from swot_rhone.plots import plot_map, plot_profile, plot_timeseries

qc = pd.read_parquet("data/processed/reach_qc.parquet")
reaches = gpd.read_parquet("data/interim/reach_raw.parquet").drop_duplicates("reach_id")
stem = set(qc["reach_id"])

figs = Path("output/figures")
figs.mkdir(parents=True, exist_ok=True)

plot_map(reaches, stem, figs / "map.png")

order = qc.groupby("reach_id")["p_dist_out"].first().sort_values(ascending=False).index.tolist()
picks = [order[0], order[len(order) // 2], order[-1]]
plot_timeseries(qc, picks, figs / "timeseries.png")

plot_profile(qc, figs / "profile.png")
print("figures saved in", figs)