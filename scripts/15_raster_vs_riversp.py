"""Compare Raster (median per reach) with RiverSP and PIXC for the chosen overpass."""

from pathlib import Path

import geopandas as gpd
import pandas as pd
import yaml

from swot_rhone.products import median_per_reach, read_raster

with open("config/rhone.yaml") as f:
    cfg = yaml.safe_load(f)
bbox = tuple(cfg["river"]["bbox"])

scenes = sorted(Path("data/raw/raster").glob("*.nc"))
raster = pd.concat([read_raster(s, bbox) for s in scenes], ignore_index=True)
raster = raster.drop_duplicates(["x", "y"])
print(len(raster), "valid water cells")
print(raster["wse"].describe())

qc = pd.read_parquet("data/processed/reach_qc.parquet")
reaches = gpd.read_parquet("data/interim/reach_raw.parquet").drop_duplicates("reach_id")
reaches = reaches[reaches["reach_id"].isin(set(qc["reach_id"]))]

per_reach = median_per_reach(raster, reaches).add_suffix("_raster")

comp = pd.read_csv("output/tables/pixc_vs_riversp.csv", dtype={"reach_id": str}).set_index("reach_id")
comp = comp.join(per_reach, how="left")
comp["diff_raster"] = comp["wse_pixc_raster"] - comp["wse"]
comp = comp.sort_values("p_dist_out", ascending=False)

cols = ["p_dist_out", "wse", "wse_pixc", "wse_pixc_raster", "diff", "diff_raster", "n_pixels_raster"]
print(comp[cols].round(2).to_string())
print("\nmedian |diff| PIXC - RiverSP (m):  ", comp["diff"].abs().median().round(3))
print("median |diff| Raster - RiverSP (m):", comp["diff_raster"].abs().median().round(3))

comp.to_csv("output/tables/three_products.csv")