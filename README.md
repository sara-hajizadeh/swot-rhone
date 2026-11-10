# swot-rhone

Water levels, slopes and discharge of the lower Rhône from SWOT satellite data.

## Project structure

```
swot-rhone/
├── config/            settings: study reaches, search area, dates
├── data/              downloaded and processed data (not in Git)
│   ├── raw/           original files, never modified
│   ├── interim/       Rhône subsets
│   └── processed/     clean, quality-controlled tables
├── src/               reusable functions
├── scripts/           workflow steps, run in order
├── tests/             tests for the functions
└── output/
    ├── figures/       plots
    ├── tables/        result tables
    └── benchmarks/    speed and memory measurements
```
