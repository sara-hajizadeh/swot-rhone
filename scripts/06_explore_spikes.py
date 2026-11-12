"""Look at the distribution of spike sizes to choose the spike threshold."""

import pandas as pd

from swot_rhone.qc import spike_size

df = pd.read_parquet("data/processed/reach_qc.parquet")
kept = df[df["qc_pass"]].copy()
kept["spike"] = spike_size(kept)

print(kept["spike"].describe(percentiles=[0.5, 0.9, 0.95, 0.99, 0.999]))
print("\nLargest spikes:")
print(kept.nlargest(10, "spike")[["reach_id", "datetime", "wse", "spike"]].to_string(index=False))