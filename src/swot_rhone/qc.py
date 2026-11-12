"""Quality control for SWOT RiverSP reach observations."""

import pandas as pd
import numpy as np

def flag_checks(df: pd.DataFrame, qc: dict) -> pd.DataFrame:
    """Return one True/False column per flag test (True = the observation fails)."""
    return pd.DataFrame(
        {
            "reach_q": df["reach_q"] > qc["max_reach_q"],
            "xovr_cal_q": df["xovr_cal_q"] > qc["max_xovr_cal_q"],
            "dark_frac": df["dark_frac"] > qc["max_dark_frac"],
        },
        index=df.index,
    )


def qc_summary(checks: pd.DataFrame) -> pd.DataFrame:
    """Count and percentage of observations failing each test, and kept overall."""
    n = len(checks)
    failed = checks.sum()
    summary = pd.DataFrame({"removed": failed, "percent": (100 * failed / n).round(1)})
    kept = (~checks.any(axis=1)).sum()
    summary.loc["kept (all tests passed)"] = [kept, round(100 * kept / n, 1)]
    return summary



def spike_size(df: pd.DataFrame) -> pd.Series:
    """How far each WSE sticks out from both neighbours in time (0 if it doesn't)."""
    df = df.sort_values(["reach_id", "datetime"])
    previous = df.groupby("reach_id")["wse"].shift(1)
    following = df.groupby("reach_id")["wse"].shift(-1)
    d_prev = df["wse"] - previous
    d_next = df["wse"] - following
    same_side = (d_prev * d_next) > 0
    return np.minimum(d_prev.abs(), d_next.abs()).where(same_side, 0.0)