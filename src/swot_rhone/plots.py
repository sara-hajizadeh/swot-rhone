"""Figures for the SWOT Rhône project."""

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import contextily as ctx

BLUE = "#2a78d6"
GREY = "#9a9a96"
BLUE = "#2a78d6"
GREY = "#9a9a96"
ORANGE = "#eb6834"
GREEN = "#1baf7a"


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



    ORANGE = "#eb6834"
GREEN = "#1baf7a"


def plot_products(pixc: pd.DataFrame, raster: pd.DataFrame, reaches: gpd.GeoDataFrame,
                  comp: pd.DataFrame, vmin: float, vmax: float, out: Path) -> None:
    """PIXC pixels, Raster cells and the per-reach comparison for one overpass."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 6), constrained_layout=True,
                             gridspec_kw={"width_ratios": [1, 1, 1.4]})

    for ax, data, title, size in [(axes[0], pixc, "PIXC water pixels", 0.1),
                                  (axes[1], raster, "Raster cells (100 m)", 1.0)]:
        sc = ax.scatter(data["longitude"], data["latitude"], c=data["wse"], s=size,
                        cmap="viridis", vmin=vmin, vmax=vmax, rasterized=True)
        reaches.plot(ax=ax, color="black", linewidth=0.4)
        ax.set_title(title)
        ax.set_xlabel("Longitude (°)")
        ax.set_ylabel("Latitude (°)")
        ax.set_aspect(1 / np.cos(np.radians(44)))
    fig.colorbar(sc, ax=axes[:2], label="WSE (m)", shrink=0.8)

    c = comp.sort_values("p_dist_out")
    km = c["p_dist_out"] / 1000
    ax = axes[2]
    ax.plot(km, c["wse"], "-o", color=BLUE, label="RiverSP")
    ax.plot(km, c["wse_pixc"], "s", color=ORANGE, mfc="none", label="PIXC (median per reach)")
    ax.plot(km, c["wse_pixc_raster"], "^", color=GREEN, mfc="none", label="Raster (median per reach)")
    ax.invert_xaxis()
    ax.set_xlabel("Distance to the sea (km)")
    ax.set_ylabel("WSE (m)")
    ax.set_title("Same overpass, three products")
    ax.legend()

    fig.savefig(out, dpi=150)
    plt.close(fig)



def plot_overpass_map(pixc: pd.DataFrame, raster: pd.DataFrame, reaches: gpd.GeoDataFrame,
                      extent: tuple[float, float, float, float],
                      vmin: float, vmax: float, out: Path) -> None:
    """Zoomed PIXC and Raster maps of one overpass on a basemap, same colour scale."""
    lon_min, lat_min, lon_max, lat_max = extent

    def crop(d: pd.DataFrame) -> gpd.GeoDataFrame:
        d = d[d["longitude"].between(lon_min, lon_max) & d["latitude"].between(lat_min, lat_max)]
        points = gpd.points_from_xy(d["longitude"], d["latitude"])
        return gpd.GeoDataFrame(d, geometry=points, crs="EPSG:4326").to_crs("EPSG:3857")

    px, rs = crop(pixc), crop(raster)
    lines = reaches.to_crs("EPSG:3857")
    corners = gpd.GeoSeries(gpd.points_from_xy([lon_min, lon_max], [lat_min, lat_max]),
                            crs="EPSG:4326").to_crs("EPSG:3857")

    fig, axes = plt.subplots(1, 2, figsize=(13, 7), constrained_layout=True)
    for ax, d, title, size in [(axes[0], px, "PIXC water pixels", 1),
                               (axes[1], rs, "Raster cells (100 m)", 6)]:
        sc = ax.scatter(d.geometry.x, d.geometry.y, c=d["wse"], s=size, marker="s",
                        linewidths=0, cmap="viridis", vmin=vmin, vmax=vmax, zorder=2)
        lines.plot(ax=ax, color="black", linewidth=0.8, zorder=3)
        ax.set_xlim(corners.x.min(), corners.x.max())
        ax.set_ylim(corners.y.min(), corners.y.max())
        ctx.add_basemap(ax, source=ctx.providers.Esri.WorldGrayCanvas, zorder=0)
        ax.set_title(f"{title} (n = {len(d):,})")
        ax.set_axis_off()
    fig.colorbar(sc, ax=axes, label="WSE (m)", shrink=0.7, extend="both")
    fig.savefig(out, dpi=200)
    plt.close(fig)