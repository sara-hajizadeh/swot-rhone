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

### Flag QC result

- Kept 2,755 of 3,892 (70.8%).
- Removed by reach_q: 276 (7.1%), xovr_cal_q: 125 (3.2%), dark_frac > 0.5: 925 (23.8%).
- Dark water is the main reason for removal. 189 rows fail more than one test.

- Reach 21602100045 median WSE (QC-passed) = 1.17 m, consistent with neighbours (1.98 m upstream, 0.90 m downstream); its spikes at −3 to −10 m are therefore errors.

### Spike test

- Spike size (on flag-passed data): median 0.04 m, 95% 1.0 m, 99% 2.84 m, max 11.0 m.
- Threshold 3 m (just above the 99th percentile).
- 9 of the 10 largest spikes are on reach 21602100045 (WSE −3 to −10 m, impossible ~67 km from the sea), recurring 2024–2026 → reach-specific problem, to investigate with PIXC/PIXCVec.

- Spike test (> 3 m): 25 removed (0.6%). Final kept: 2,730 of 3,892 (70.1%).

- **Open questions:** …

### Figures

- Profile: 107 passes covering ≥70% of the main channel. Three dam steps at ~119, ~98 and ~72 km; flat pools between them.
- Variability is large at the upstream end of pools (e.g. 39–45 m at 152 km) and small just upstream of dams (level held by operation).
- Reach 21602300881 (152 km): flood peaks up to +5 m.
- Reach 21602300041 (100 km, upstream of a dam): stable ~25 m with drops to ~22 m at flood times → likely pool drawdown during floods (to confirm with CNR operations).
- Reach 21602100025 (59 km, below the last dam): −0.4 to +4.4 m, follows floods → free-flowing.

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
