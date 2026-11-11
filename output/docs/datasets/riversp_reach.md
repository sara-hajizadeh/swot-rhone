### Attributes (128 columns)

One row = one reach observed in one pass.

| Group              | Examples                                              | Meaning                            |
| ------------------ | ----------------------------------------------------- | ---------------------------------- |
| Identity           | reach_id, river_name                                  | Which reach                        |
| Time               | time, time_tai, time_str                              | When it was observed (UTC)         |
| Measurements       | wse, slope, width, area_total                         | What SWOT measured                 |
| Uncertainty        | wse_u, wse_r_u, slope_u, width_u                      | Product's own uncertainty estimate |
| Quality flags      | reach_q, dark_frac, xovr_cal_q, ice_clim_f, partial_f | How good the observation is        |
| Corrections        | geoid_hght, solid_tide, dry_trop_c, wet_trop_c        | Corrections already applied        |
| SWORD priors (p\_) | p_wse, p_width, p_dist_out, p_n_nodes, p_dam_id       | Fixed values from SWORD            |
| Topology           | rch_id_up, rch_id_dn, n_reach_up, n_reach_dn          | Upstream/downstream neighbours     |
| Discharge          | dschg_c, dschg_m, ...                                 | Modelled discharge (not measured)  |

Reference: SWOT RiverSP Product Description (PO.DAAC).

### Topology

- `rch_id_dn` / `rch_id_up`: neighbour reach IDs as one text, comma-separated; `no_data` = no neighbour.
- Check: reach 21602100025 → rch_id_dn = 21602100015, 21602100555, no_data, no_data
- Meaning: two downstream reaches = the split at Arles (Grand Rhône / Petit Rhône).

### Fill values

- Missing numbers : -999999999999.0
- Missing time: time_str = "no_data": 2742.
