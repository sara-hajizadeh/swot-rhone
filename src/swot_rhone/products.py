"""Read SWOT PIXC and Raster products."""

from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
import geopandas as gpd

PIXC_VARS = ["height", "geoid", "solid_earth_tide", "load_tide_fes", "pole_tide",
             "water_frac", "pixel_area"]

RASTER_VARS = ["latitude", "longitude", "wse", "wse_qual", "wse_uncert", "water_frac", "n_wse_pix"]


def read_pixc(path: Path, bbox: tuple[float, float, float, float],
              classes: tuple[int, ...] = (3, 4)) -> pd.DataFrame:
    """Read water pixels of one PIXC tile inside the bbox, with WSE above the geoid."""
    with xr.open_dataset(path, group="pixel_cloud") as ds:
        lon = ds["longitude"].values
        lat = ds["latitude"].values
        cls = ds["classification"].values

        lon_min, lat_min, lon_max, lat_max = bbox
        keep = ((lon >= lon_min) & (lon <= lon_max) & (lat >= lat_min) & (lat <= lat_max)
                & np.isin(cls, classes))
        idx = np.flatnonzero(keep)
        sub = ds[PIXC_VARS].isel(points=idx).load()

    df = sub.to_dataframe().reset_index(drop=True)
    df["classification"] = cls[idx]
    df["wse"] = (df["height"] - df["geoid"] - df["solid_earth_tide"]
                 - df["load_tide_fes"] - df["pole_tide"])
    df["tile"] = path.stem.split("_")[6]
    return df.dropna(subset=["wse"])

def  median_per_reach(pixc: pd.DataFrame, reaches: gpd.GeoDataFrame,
                   max_dist: float = 300.0) -> pd.DataFrame:
    """Assign pixels to the nearest reach within max_dist metres; median WSE per reach."""
    points = gpd.GeoDataFrame(
        pixc, geometry=gpd.points_from_xy(pixc["longitude"], pixc["latitude"]), crs="EPSG:4326"
    ).to_crs("EPSG:32631")
    lines = reaches[["reach_id", "geometry"]].to_crs("EPSG:32631")

    joined = gpd.sjoin_nearest(points, lines, max_distance=max_dist, how="inner")
    return joined.groupby("reach_id").agg(n_pixels=("wse", "size"), wse_pixc=("wse", "median"))




def read_raster(path: Path, bbox: tuple[float, float, float, float],
                max_qual: int = 1) -> pd.DataFrame:
    """Read Raster cells with a valid WSE inside the bbox."""
    with xr.open_dataset(path) as ds:
        df = ds[RASTER_VARS].to_dataframe().reset_index()

    lon_min, lat_min, lon_max, lat_max = bbox
    inside = df["longitude"].between(lon_min, lon_max) & df["latitude"].between(lat_min, lat_max)
    df = df[inside & df["wse"].notna() & (df["wse_qual"] <= max_qual)].copy()
    df["scene"] = path.stem.split("_")[12]
    return df

