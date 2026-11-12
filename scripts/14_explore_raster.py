"""Look at the structure of one Raster file."""

from pathlib import Path

import xarray as xr

f = sorted(Path("data/raw/raster").glob("*.nc"))[0]
print(f.name)

ds = xr.open_dataset(f)
print(ds)

for v in ["wse", "wse_qual", "wse_uncert", "water_frac", "n_wse_pix"]:
    if v in ds:
        print(f"\n{v}: {ds[v].attrs.get('long_name')} [{ds[v].attrs.get('units')}]")
        print(f"  {ds[v].attrs.get('comment')}")
    else:
        print(f"\n{v}: NOT FOUND")