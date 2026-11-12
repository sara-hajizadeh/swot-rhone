"""Figure: PIXC, Raster and RiverSP for the chosen overpass."""

from pathlib import Path

import geopandas as gpd
import pandas as pd
import yaml

from swot_rhone.plots import plot_products
from swot_rhone.products import read_raster

with open("config/rhone.yaml") as f:
    cfg = yaml.safe_load(f)
bbox = tuple(cfg["river"]["bbox"])

pixc = pd.read_parquet("data/interim/pixc_overpass.parquet")
scenes = sorted(Path("data/raw/raster").glob("*.nc"))
raster = pd.concat([read_raster(s, bbox) for s in scenes]).drop_duplicates(["x", "y"])

comp = pd.read_csv("output/tables/three_products.csv", dtype={"reach_id": str})
qc = pd.read_parquet("data/processed/reach_qc.parquet")
reaches = gpd.read_parquet("data/interim/reach_raw.parquet").drop_duplicates("reach_id")
reaches = reaches[reaches["reach_id"].isin(set(qc["reach_id"]))]

vmin, vmax = comp["wse"].min() - 2, comp["wse"].max() + 2
plot_products(pixc, raster, reaches, comp, vmin, vmax, Path("output/figures/three_products.png"))
print("saved output/figures/three_products.png")
