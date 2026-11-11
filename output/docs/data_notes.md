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
