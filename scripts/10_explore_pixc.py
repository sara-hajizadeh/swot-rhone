"""Look at the structure of one PIXC file."""

from pathlib import Path

import xarray as xr

f = sorted(Path("data/raw/pixc").glob("*.nc"))[0]
print(f.name)

ds = xr.open_dataset(f, group="pixel_cloud")
print(list(ds.data_vars))

wanted = ["height", "geoid", "classification", "water_frac", "pixel_area",
          "geolocation_qual", "classification_qual",
          "solid_earth_tide", "load_tide_fes", "pole_tide", "height_cor_xover"]
for v in wanted:
    if v in ds:
        print(f"{v}: {ds[v].attrs.get('long_name')} [{ds[v].attrs.get('units')}]")
    else:
        print(f"{v}: NOT FOUND")

print(ds["classification"].attrs.get("flag_values"))
print(ds["classification"].attrs.get("flag_meanings"))


#For checking WSE ≈ ??
for v in ["height", "height_cor_xover", "geoid", "solid_earth_tide", "load_tide_fes", "pole_tide"]:
    print(f"\n{v}:\n  {ds[v].attrs.get('comment')}")
