"""Read the PIXC tiles of the chosen overpass and keep Rhône water pixels."""

from pathlib import Path

import pandas as pd
import yaml

from swot_rhone.products import read_pixc

with open("config/rhone.yaml") as f:
    cfg = yaml.safe_load(f)
bbox = tuple(cfg["river"]["bbox"])

tiles = sorted(Path("data/raw/pixc").glob("*.nc"))
pixc = pd.concat([read_pixc(t, bbox) for t in tiles], ignore_index=True)

print(len(pixc), "water pixels")
print(pixc["tile"].value_counts())
print(pixc["classification"].value_counts())
print(pixc["wse"].describe())

pixc.to_parquet("data/interim/pixc_overpass.parquet")