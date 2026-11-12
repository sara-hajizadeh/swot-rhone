"""Compare PIXC (median per reach) with RiverSP for the chosen overpass."""

import geopandas as gpd
import pandas as pd
import yaml

from swot_rhone.products import pixc_per_reach

with open("config/rhone.yaml") as f:
    cfg = yaml.safe_load(f)
ov = cfg["overpass"]

pixc = pd.read_parquet("data/interim/pixc_overpass.parquet")
qc = pd.read_parquet("data/processed/reach_qc.parquet")
stem = set(qc["reach_id"])
reaches = gpd.read_parquet("data/interim/reach_raw.parquet").drop_duplicates("reach_id")
reaches = reaches[reaches["reach_id"].isin(stem)]

per_reach = pixc_per_reach(pixc, reaches)

river = qc[(qc["cycle"] == ov["cycle"]) & (qc["pass_id"] == ov["pass_id"])]
river = river.set_index("reach_id")[["p_dist_out", "wse", "qc_pass"]]

comp = river.join(per_reach, how="inner")
comp["diff"] = comp["wse_pixc"] - comp["wse"]
comp = comp.sort_values("p_dist_out", ascending=False)
print(comp.round(2).to_string())
print("\nmedian |diff| (m):", comp["diff"].abs().median().round(3))

comp.to_csv("output/tables/pixc_vs_riversp.csv")