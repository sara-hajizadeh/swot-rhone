"""Read all downloaded Reach files and keep the study area."""

from pathlib import Path
import yaml
from swot_rhone.riversp import clean_reaches, main_channel, read_reaches
with open("config/rhone.yaml") as f:
    cfg = yaml.safe_load(f)

files = sorted(Path("data/raw/riversp_reach").glob("*.zip"))   # all .zip files
reaches = read_reaches(files, tuple(cfg["river"]["bbox"]))
print(reaches.shape, "rows/columns,", reaches["reach_id"].nunique(), "reaches")

reaches.to_parquet("data/interim/reach_raw.parquet")
stem = main_channel(reaches, cfg["river"]["start_reach"], cfg["river"]["end_reach"])
print(len(stem), "main-channel reaches:", stem)
clean = clean_reaches(reaches, stem)
print(len(clean), "observations on", clean["reach_id"].nunique(), "main-channel reaches")
clean.to_parquet("data/interim/reach_clean.parquet")
