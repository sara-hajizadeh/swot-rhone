# Data notes

Running notes on each dataset: what it is, how I got it, what I found, and the decisions I made.

## 1. SWOT RiverSP (Reach)

- **Product:** SWOT_L2_HR_RiverSP_D (version D), Reach files, Europe (EU)
- **Access:** PO.DAAC through earthaccess, filtered by bbox, dates and file name `*Reach*_EU_*`
- **Period:** 2023-07-21 (start of science orbit) to today
- **Volume:** 1,136 files, ~6 GB (each file = one pass over Europe)
- **Read:** 16,389 rows × 128 columns, 68 reaches inside the bbox
- **Findings:**
  - The first search mixed Reach and Node files → filtered by file name.
  - An older download included 9 Cal/Val files (cycles ≥ 400) → removed.
  - The bbox includes tributaries (Gardon, Durance, Cèze) → main channel selected by SWORD topology.

### Flags (3,892 clean observations)

- reach_q: 0=105, 1=3,511, 2=275, 3=1 → keep ≤1 (keeping only 0 would lose 97%).
- xovr_cal_q: 0=3,748, 1=19, 2=125 → keep ≤1.
- ice_clim_f: -999 (not available)=2,280, 0=1,612, no ice → not used. Note: -999 is a second fill value for integer flags.
- partial_f: 280 partial → kept, to test later.
- dark_frac: median 0.06, 75th percentile 0.47 → remove > 0.5.
- wse_u: median 0.11 m, max 0.86 m.

- **Open questions:** …

## 2. SWOT RiverSP (Node)

- **Plan:** Hydrocron API, Rhône nodes only (full Node files ≈ 36 GB)
- **Findings:** …

## 3. SWOT PIXC

- **Search:** 630 files, ~400 GB for the full period (~630 MB per tile)
- **Decision:** one pass, one date only
- **Findings:** …

## 4. SWOT Raster

- **Search:** 2,542 files, ~86 GB
- **Findings:** the spatial search returned scenes from other UTM zones (e.g. UTM60W). The Rhône is in UTM31T → filtered by file name `*_100m_UTM31T_*`.

## 5. SWORD

- **Used for:** reach IDs, topology (`rch_id_dn`), reach type (last digit), dams
- **Findings:** many main-channel reaches have no name (`no_data`), so I don't select by name.

## 6. Gauge stations (Hub'Eau)

- …
