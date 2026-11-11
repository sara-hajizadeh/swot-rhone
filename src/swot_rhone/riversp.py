"""Read SWOT RiverSP files."""

from pathlib import Path

import geopandas as gpd
import pandas as pd


def read_reaches(files: list[Path], bbox: tuple[float, float, float, float]) -> gpd.GeoDataFrame:
    """Read zipped RiverSP Reach shapefiles and keep reaches inside the bbox."""
    frames = []
    for f in files:
        gdf = gpd.read_file(f"zip://{f}", bbox=bbox)
        if gdf.empty:
            continue
        gdf["granule"] = f.stem          # the file name without ".zip" (hint: f.stem)
        frames.append(gdf)
    return gpd.GeoDataFrame(pd.concat(frames, ignore_index=True), crs=frames[0].crs)