"""Search SWOT files for the study area and period, without downloading."""

import earthaccess
import yaml
from datetime import date

PRODUCTS = ["SWOT_L2_HR_RiverSP_D", "SWOT_L2_HR_PIXC_D", "SWOT_L2_HR_Raster_D"]
with open("config/rhone.yaml") as f:
    cfg = yaml.safe_load(f) 

bbox= tuple(cfg["river"]["bbox"])
end = cfg["time"]["end"] or date.today().isoformat()
dates = (cfg["time"]["start"], end)
earthaccess.login(strategy="netrc")
for product in PRODUCTS:
    results = earthaccess.search_data(short_name=product, bounding_box=bbox, temporal=dates)
    total_gb = sum(g.size for g in results) / 1024   # size() is in MB
    print(f"{product}: {len(results)} files, {total_gb:.1f} GB")
    if results:
        print("   first:", results[0]["meta"]["native-id"])

    