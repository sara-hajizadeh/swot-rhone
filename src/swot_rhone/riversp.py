"""Read SWOT RiverSP files."""

from pathlib import Path

import geopandas as gpd
import pandas as pd

FILL = -1e9   # SWOT fill value is -999999999999; anything below this is "missing"
GRANULE = r"Reach_(?P<cycle>\d{3})_(?P<pass_id>\d{3})_\w{2}_.*_(?P<crid>P\w{3})_(?P<counter>\d{2})$"


def read_reaches(files: list[Path], bbox: tuple[float, float, float, float]) -> gpd.GeoDataFrame:
    """Read zipped RiverSP Reach shapefiles and keep reaches inside the bbox."""
    frames = []
    for f in files:
        gdf = gpd.read_file(f"zip://{f}", bbox=bbox)
        if gdf.empty:      
            continue     #some passes don’t cover the Rhône at all
        gdf["granule"] = f.stem          # the file name without ".zip" (hint: f.stem)
        frames.append(gdf)
    if not frames:
        raise ValueError("no reaches found inside the bbox")
    return gpd.GeoDataFrame(pd.concat(frames, ignore_index=True), crs=frames[0].crs)

def neighbours(text: str) -> list[str]:   #clean list of reach IDs
    """Split a SWORD neighbour field like '216..., 216..., no_data' into reach ids."""
    return [r.strip() for r in str(text).split(",") if r.strip() not in ("", "no_data")]


def main_channel(reaches: pd.DataFrame, start: str, end: str) -> list[str]:
    """Follow downstream links from start to end and return the reach ids on the way."""
    info = reaches.drop_duplicates("reach_id")
    down = dict(zip(info["reach_id"].astype(str), info["rch_id_dn"].map(neighbours)))
    path = [start]
    while path[-1] != end:
        options = [r for r in down.get(path[-1], []) if r in down and r not in path]
        if not options:
            raise ValueError(f"no downstream path from {path[-1]} to {end}")
        path.append(options[0])
    return path


def clean_reaches(reaches: pd.DataFrame, stem: list[str]) -> pd.DataFrame:
    """Keep main-channel reaches with a real observation, one row per reach and pass."""
    df = reaches[reaches["reach_id"].isin(stem)].copy()

    numeric = df.select_dtypes("number").columns
    df[numeric] = df[numeric].mask(df[numeric] < FILL)
    df = df.copy()
    df["datetime"] = pd.to_datetime(df["time_str"], utc=True, errors="coerce", format="ISO8601")
    df = df.dropna(subset=["datetime", "wse"])

    df = df.join(df["granule"].str.extract(GRANULE)).copy()
    df["rank"] = (df["crid"].str[1] == "G") * 100 + df["counter"].astype(int)
    df = df.sort_values("rank").drop_duplicates(["reach_id", "cycle", "pass_id"], keep="last")

    return df.drop(columns="rank").sort_values(["reach_id", "datetime"]).reset_index(drop=True)