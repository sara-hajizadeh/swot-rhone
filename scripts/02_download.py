"""Download SWOT RiverSP Reach files for the study area and period."""

from datetime import date
from pathlib import Path

import earthaccess
import yaml

with open("config/rhone.yaml") as f:
    cfg = yaml.safe_load(f)

bbox = tuple(cfg["river"]["bbox"])
end = cfg["time"]["end"] or date.today().isoformat()
dates = (cfg["time"]["start"], end)

out_dir = Path("data/raw/riversp_reach")
out_dir.mkdir(parents=True, exist_ok=True)

earthaccess.login(strategy="netrc")
results = earthaccess.search_data(
    short_name="SWOT_L2_HR_RiverSP_D",
    granule_name="*Reach*_EU_*",            # only Reach files for Europe
    bounding_box=bbox,
    temporal=dates,
)
print(len(results), "files to download")

files = earthaccess.download(results, local_path=str(out_dir), threads=8)
print(len(files), "files downloaded to", out_dir)