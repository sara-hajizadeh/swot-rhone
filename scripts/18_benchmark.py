"""Benchmark reading RiverSP Reach files: baseline vs needed columns vs parallel."""

import os
import platform
import time
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from pathlib import Path

import pandas as pd
import yaml

from swot_rhone.riversp import read_one, read_reaches

COLUMNS = ["reach_id", "river_name", "time_str", "wse", "wse_u", "slope", "width",
           "reach_q", "xovr_cal_q", "dark_frac", "ice_clim_f", "partial_f",
           "p_dist_out", "p_n_nodes", "p_dam_id", "rch_id_up", "rch_id_dn"]


def read_parallel(files: list[Path], bbox: tuple, columns: list[str], workers: int) -> pd.DataFrame:
    """Read files in parallel processes and concatenate the non-empty results."""
    with ProcessPoolExecutor(max_workers=workers) as pool:
        frames = list(pool.map(partial(read_one, bbox=bbox, columns=columns), files))
    return pd.concat([f for f in frames if not f.empty], ignore_index=True)


def timed(label: str, func) -> tuple[pd.DataFrame, dict]:
    """Run func, return its result and a row with time, size and memory."""
    start = time.perf_counter()
    df = func()
    seconds = time.perf_counter() - start
    mb = df.memory_usage(deep=True).sum() / 1e6
    print(f"{label:<32} {seconds:7.1f} s  {len(df):>6} rows  {df.shape[1]:>4} cols  {mb:7.1f} MB")
    return df, {"version": label, "seconds": round(seconds, 1), "rows": len(df),
                "columns": df.shape[1], "table_mb": round(mb, 1)}


if __name__ == "__main__":
    with open("config/rhone.yaml") as f:
        cfg = yaml.safe_load(f)
    bbox = tuple(cfg["river"]["bbox"])
    files = sorted(Path("data/raw/riversp_reach").glob("*.zip"))
    workers = os.cpu_count()
    print(f"{len(files)} files, {platform.processor() or platform.machine()}, {workers} CPU cores\n")

    a, row_a = timed("A. baseline (all columns)", lambda: read_reaches(files, bbox))
    b, row_b = timed("B. needed columns", lambda: read_reaches(files, bbox, COLUMNS))
    c, row_c = timed(f"C. B + {workers} processes", lambda: read_parallel(files, bbox, COLUMNS, workers))

    key = ["granule", "reach_id", "wse"]
    same = (a[key].sort_values(key[:2]).reset_index(drop=True)
            .equals(c[key].sort_values(key[:2]).reset_index(drop=True)))
    print("\nC gives the same rows and WSE values as A:", same)

    out = Path("output/benchmarks")
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([row_a, row_b, row_c]).to_csv(out / "read_benchmark.csv", index=False)