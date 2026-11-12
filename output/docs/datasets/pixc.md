# SWOT PIXC (version D)

- Group `pixel_cloud`: one tile ≈ 6.3 million pixels, 62 variables (~2 GB if fully loaded).
- Classes (from file): 1 land, 2 land_near_water, 3 water_near_land, 4 open_water, 5 dark_water, 6 low_coh_water_near_land, 7 open_low_coh_water. Used: 3 and 4.
- `height` is above the ellipsoid. `height_cor_xover` is already applied.
- geoid, solid_earth_tide, load_tide_fes and pole_tide are NOT applied →
  WSE = height − geoid − solid_earth_tide − load_tide_fes − pole_tide.
- geolocation_qual and classification_qual are bitwise flags (not used yet).
