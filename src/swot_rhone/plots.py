"""Figures for the SWOT Rhône project."""

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

BLUE = "#2a78d6"
GREY = "#9a9a96"


def plot_map(reaches: gpd.GeoDataFrame, stem: set[str], out: Path) -> None:
    """Map of all reaches in the bbox, with the main channel highlighted."""
    fig, ax = plt.subplots(figsize=(5, 7))
    reaches.plot(ax=ax, color=GREY, linewidth=1)
    reaches[reaches["reach_id"].isin(stem)].plot(ax=ax, color=BLUE, linewidth=2.5)
    ax.set_title("Lower Rhône: SWORD reaches (main channel in blue)")
    ax.set_xlabel("Longitude (°)")
    ax.set_ylabel("Latitude (°)")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_timeseries(df: pd.DataFrame, reach_ids: list[str], out: Path) -> None:
    """WSE over time for a few reaches: kept and removed observations."""
    fig, axes = plt.subplots(len(reach_ids), 1, figsize=(9, 2.5 * len(reach_ids)), sharex=True)
    for ax, rid in zip(axes, reach_ids):
        d = df[df["reach_id"] == rid].sort_values("datetime")
        kept = d[d["qc_pass"]]
        removed = d[~d["qc_pass"]]
        ax.plot(removed["datetime"], removed["wse"], "x", color=GREY, ms=4, label="Removed by QC")
        ax.plot(kept["datetime"], kept["wse"], "-o", color=BLUE, ms=3, lw=1, label="Kept")
        low, high = kept["wse"].quantile([0.01, 0.99])
        ax.set_ylim(low - 1, high + 1)
        km = d["p_dist_out"].iloc[0] / 1000
        ax.set_title(f"Reach {rid} ({km:.0f} km from the sea)")
        ax.set_ylabel("WSE (m)")
    axes[0].legend()
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def plot_profile(df: pd.DataFrame, out: Path, min_cover: float = 0.7) -> None:
    """WSE along the river: one line per pass, plus the median profile."""
    kept = df[df["qc_pass"]]
    n_reaches = kept["reach_id"].nunique()
    fig, ax = plt.subplots(figsize=(9, 4.5))

    n_passes = 0
    for _, p in kept.groupby(["cycle", "pass_id"]):
        if p["reach_id"].nunique() < min_cover * n_reaches:
            continue
        p = p.sort_values("p_dist_out")
        ax.plot(p["p_dist_out"] / 1000, p["wse"], color=GREY, lw=0.5, alpha=0.5)
        n_passes += 1

    median = kept.groupby("reach_id").agg(x=("p_dist_out", "first"), wse=("wse", "median"))
    median = median.sort_values("x")
    ax.plot(median["x"] / 1000, median["wse"], "-o", color=BLUE, lw=2, ms=4, label="Median of all passes")
    ax.plot([], [], color=GREY, label=f"Single passes (n = {n_passes})")

    ax.invert_xaxis()
    ax.set_xlabel("Distance to the sea (km)")
    ax.set_ylabel("WSE (m)")
    ax.set_title("Longitudinal profile of the lower Rhône (SWOT RiverSP)")
    ax.legend()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)