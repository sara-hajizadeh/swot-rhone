"""Download PIXC and Raster files for the chosen overpass."""

from datetime import date, timedelta
from pathlib import Path

import earthaccess
import yaml

with open("config/rhone.yaml") as f:
    cfg = yaml.safe_load(f)

ov = cfg["overpass"]
bbox = tuple(cfg["river"]["bbox"])
day = date.fromisoformat(ov["date"])
temporal = (day.isoformat(), (day + timedelta(days=1)).isoformat())
cycle_pass = f"{ov['cycle']}_{ov['pass_id']}"

PRODUCTS = {
    "pixc": ("SWOT_L2_HR_PIXC_D", f"*_{cycle_pass}_*"),
    "raster": ("SWOT_L2_HR_Raster_D", f"*_100m_UTM31T_*_{cycle_pass}_*"),
}

earthaccess.login(strategy="netrc")

for name, (short_name, pattern) in PRODUCTS.items():
    results = earthaccess.search_data(
        short_name=short_name, granule_name=pattern, bounding_box=bbox, temporal=temporal
    )
    print(f"{name}: {len(results)} files, {sum(g.size for g in results):.0f} MB")
    for g in results:
        print("   ", g["meta"]["native-id"])

    out = Path("data/raw") / name
    out.mkdir(parents=True, exist_ok=True)
    earthaccess.download(results, local_path=str(out), threads=4)
    