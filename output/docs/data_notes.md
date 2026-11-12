# Data notes

Running notes on each dataset: what it is, how I got it, what I found, and the decisions I made.

## 1. SWOT RiverSP (Reach)

- **Product:** SWOT_L2_HR_RiverSP_D (version D), Reach files, Europe (EU)
- **Access:** PO.DAAC through earthaccess, filtered by bbox, dates and file name `*Reach*_EU_*`
- **Period:** 2023-07-21 (start of science orbit) to today
- **Volume:** 1,145 files (~6 GB): 1,136 from the science orbit + 9 Cal/Val files (cycles ≥ 400)
  from an older download. Checked: 0 observations before 2023-07-21 remain after cleaning.
- **Read:** 16,389 rows × 128 columns, 68 reaches inside the bbox
- **Findings:**
  - The first search mixed Reach and Node files → filtered by file name.
  - An older download included 9 Cal/Val files (cycles ≥ 400) → removed.
  - The bbox includes tributaries (Gardon, Durance, Cèze) → main channel selected by SWORD topology.

### Main channel and cleaning

- Main channel: 20 reaches from 21602300881 to 21602100025 (following SWORD downstream links).
- 2,742 of 16,389 rows (17%) have no observation (time_str = "no_data"); fill value = -999999999999.
- After cleaning (fills, empty passes, duplicate processing versions): 3,892 observations on 19 reaches.
  The dam reach 21602100034 has no valid WSE.

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

### Spike test

- Spike size (on flag-passed data): median 0.04 m, 95% 1.0 m, 99% 2.84 m, max 11.0 m.
- Threshold 3 m (just above the 99th percentile).
- 9 of the 10 largest spikes are on reach 21602100045 (WSE −3 to −10 m, impossible ~67 km from the sea),
  recurring 2024–2026 → reach-specific problem, to investigate with PIXC/PIXCVec.
- Reach 21602100045 median WSE (QC-passed) = 1.17 m, consistent with neighbours (1.98 m upstream,
  0.90 m downstream); its spikes at −3 to −10 m are therefore errors.
- Spike test (> 3 m): 25 removed (0.6%). Final kept: 2,730 of 3,892 (70.1%).
- Limitation: 2 impossible values remain on reach 21602100045 (−3.14 m on 2023-09-21, −1.91 m on
  2026-10-01). The spike test misses consecutive or edge errors. Possible fix: a per-reach outlier
  test based on the distance from the reach median.

### Figures

- Profile: 107 passes covering ≥70% of the main channel. Three dam steps at ~119, ~98 and ~72 km;
  flat pools between them.
- Variability is large at the upstream end of pools (e.g. 39–45 m at 152 km) and small just
  upstream of dams (level held by operation).
- Reach 21602300881 (152 km): flood peaks up to +5 m.
- Reach 21602300041 (100 km, upstream of a dam): stable ~25 m with drops to ~22 m at flood times
  → likely pool drawdown during floods (to confirm with CNR operations).
- Reach 21602100025 (59 km, below the last dam): −0.4 to +4.4 m, follows floods → free-flowing.

## 2. SWOT RiverSP (Node)

- Not used in this version. The product comparison was done with PIXC per reach instead.
- Option for later: Hydrocron API for Rhône nodes only (full Node files ≈ 36 GB for the area).

## 3. SWOT PIXC

- **Search:** 630 files, ~400 GB for the full period (~630 MB per tile).
- **Decision:** one pass, one date only.
  - Why: downloading the full period is not possible on a laptop, and one overpass is enough to
    compare PIXC with Raster and RiverSP.
  - How the overpass was chosen: from the QC'd RiverSP data, ranking passes by number of
    main-channel reaches observed, then by median dark_frac (scripts/08_choose_overpass.py).
  - Chosen: cycle 024, pass 292, 2024-11-22 (19/19 reaches, median dark_frac 0.0076).
- **Downloaded:** 3 tiles (077L, 078L, 078R), 2,108 MB. The river section is observed in ~20 s.
- **Structure:** one tile ≈ 6.3 million pixels and 62 variables (~2 GB if fully loaded),
  so only the needed variables and pixels are loaded.
- **WSE:** height − geoid − solid_earth_tide − load_tide_fes − pole_tide
  (height_cor_xover is already applied; confirmed from the variable comments in the file).
- **Classes kept:** 3 (water_near_land) and 4 (open_water). Dark water (5) excluded.
- **Findings:**
  - 449,600 water pixels (classes 3+4) in the bbox; 077L 290,789, 078L 158,811, 078R 0
    (the Rhône is entirely on the left swath for this pass).
  - 59% class 3 (water near land): the river is narrow, so many pixels touch a bank.
  - WSE: median 25.0 m (matches the ~25 m pool level in RiverSP), but min −31 m and max 1,219 m:
    single pixels are noisy, and the bbox includes other water bodies → per-reach median needed.
  - Many class 3/4 pixels far from the river, with heights following the terrain (≥40 m on hills,
    ~0 m in the Camargue): real water in the south (lagoons, marshes), elsewhere probably land
    classified as water. Horizontal stripes near 43.65–43.70° look like swath artefacts.
  - Only ~97,000 of 449,600 water pixels (~22%) lie within 300 m of the main channel.

## 4. SWOT Raster

- **Search (full period, bbox):** 2,542 files, ~86 GB.
- **Finding:** the spatial search returned scenes from other UTM zones (e.g. UTM60W).
  The Rhône is in UTM31T → filtered by file name `*_100m_UTM31T_*`.
- **Decision:** same overpass as PIXC (cycle 024, pass 292, 2024-11-22), 100 m resolution.
- **Downloaded:** 2 scenes (038F, 039F), 117 MB, about 18 times smaller than PIXC for the same overpass.
- **Findings:**
  - 65,896 valid water cells (wse_qual ≤ 1) in the bbox; WSE −29 to 315 m
    (other water bodies included → selection by distance to the main channel).
  - Isolated false water detections on land appear as single pixels in PIXC but as full 100 m
    cells in Raster.

## 5. Product comparison (one overpass: 024/292, 2024-11-22)

- Method: median WSE of PIXC pixels / Raster cells within 300 m of each main-channel reach
  (spatial approximation; the official assignment is in PIXCVec).
- PIXC vs RiverSP: median |diff| = 0.027 m; Raster vs RiverSP: 0.032 m (19 reaches)
  → for normal reaches the three products agree within a few cm.
- Large differences only at the three dam reaches (PIXC: +3.51 m at 119 km, −3.18 m at 98 km,
  −3.04 m at 72 km): a reach containing a 9–13 m step has no single meaningful WSE.
  Reach 21602300091: PIXC +3.51 m but Raster −1.94 m vs RiverSP → the value depends on which
  pixels/cells fall on each side of the step.
- Reach 21602300881: PIXC −1.86 m, Raster −1.23 m because the bbox (north edge 44.30°) cuts the
  reach → limitation of my setup; fix by extending the bbox.
- 46–828 Raster cells per reach vs 794–19,146 PIXC pixels: much less data, same answer.
- Figure three_products.png: PIXC/Raster medians lie on the RiverSP profile except at the dam reaches.
- Zoom map around Avignon: the ~10 m dam step at ~98 km is visible in space (≈ 25 m upstream,
  ≈ 15 m downstream). The Durance shows a gradual colour change = continuous slope of a natural
  river, unlike the flat pools and steps of the Rhône.

## 6. SWORD

- **Used for:** reach IDs, topology (`rch_id_dn`), reach type (last digit), dams.
- **Findings:**
  - Many main-channel reaches have no name (`no_data`), so I don't select by name.
  - Neighbour fields always have 4 slots, padded with `no_data`.
  - Last digit 4 = dam (e.g. 21602100034); these reaches have no valid WSE.
  - TODO: note which SWORD version RiverSP version D uses.

## 7. Gauge stations (Hub'Eau)

- Not done yet.

## 8. Benchmark: reading RiverSP Reach files (scripts/18_benchmark.py)

- Input: 1,145 zipped shapefiles (~6 GB), bbox filter. Hardware: Apple Silicon (arm), 10 CPU cores.
- A. Baseline (all 128 columns, sequential): 20.8 s, 17.9 MB table.
- B. Needed columns only (19): 19.3 s (1.1×), 5.2 MB (−71% memory).
- C. B + 10 processes: 5.3 s (3.9×), same 5.2 MB.
- Correctness: C gives exactly the same rows and WSE values as A.
- Interpretation: time is dominated by opening each file and filtering by bbox, not by parsing
  columns; parallel speed-up is below 10× because of process overhead, shared disk access and
  the serial concatenation.
- Results saved in output/benchmarks/read_benchmark.csv.

- Two runs gave nearly identical times (A 20.8 / 20.3 s, C 5.3 / 5.2 s): results are reproducible,
  the disk cache has little effect, and the work is CPU-bound (unzipping, spatial filtering),
  which is why parallel processes help.

## Open questions

- Reach 21602100045: why recurring values at −3 to −10 m? Check with PIXC/PIXCVec (pixels from below
  the dam assigned to this reach? layover?).
- Pool drawdown during floods at reach 21602300041: confirm with CNR operating information.
- Should reaches be split at dams, so that each part has a meaningful WSE?
- Does removing partial_f = 1 observations change the results (sensitivity test)?
