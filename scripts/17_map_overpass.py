"""Zoomed map of PIXC and Raster for the chosen overpass."""

from pathlib import Path

import geopandas as gpd
import pandas as pd
import yaml
from shapely.geometry import box

from swot_rhone.plots import plot_overpass_map
from swot_rhone.products import read_raster

with open("config/rhone.yaml") as f:
    cfg = yaml.safe_load(f)
bbox = tuple(cfg["river"]["bbox"])
extent = tuple(cfg["figures"]["zoom_extent"])

pixc = pd.read_parquet("data/interim/pixc_overpass.parquet")
scenes = sorted(Path("data/raw/raster").glob("*.nc"))
raster = pd.concat([read_raster(s, bbox) for s in scenes]).drop_duplicates(["x", "y"])

qc = pd.read_parquet("data/processed/reach_qc.parquet")
reaches = gpd.read_parquet("data/interim/reach_raw.parquet").drop_duplicates("reach_id")
reaches = reaches[reaches["reach_id"].isin(set(qc["reach_id"]))]

comp = pd.read_csv("output/tables/three_products.csv", dtype={"reach_id": str}).set_index("reach_id")
in_zoom = reaches.loc[reaches.intersects(box(*extent)), "reach_id"]
wse = comp.loc[comp.index.intersection(in_zoom), "wse"]
vmin, vmax = wse.min() - 1, wse.max() + 1
print("reaches in zoom:", list(in_zoom))
print("colour range:", round(vmin, 1), "to", round(vmax, 1), "m")

out = Path("output/figures/overpass_map_avignon.png")
plot_overpass_map(pixc, raster, reaches, extent, vmin, vmax, out)
print("saved", out)