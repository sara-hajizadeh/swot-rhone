"""Read all downloaded Reach files and keep the study area."""

from pathlib import Path
import yaml
from swot_rhone.riversp import read_reaches

with open("config/rhone.yaml") as f:
    cfg = yaml.safe_load(f)

files = sorted(Path("data/raw/riversp_reach").glob("*.zip"))   # all .zip files
reaches = read_reaches(files, tuple(cfg["river"]["bbox"]))
print(reaches.shape, "rows/columns,", reaches["reach_id"].nunique(), "reaches")

reaches.to_parquet("data/interim/reach_raw.parquet")