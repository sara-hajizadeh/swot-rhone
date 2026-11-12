"""Tests for the core processing functions, on small hand-made examples."""

import pandas as pd
import pytest

from swot_rhone.qc import flag_checks, spike_size
from swot_rhone.riversp import main_channel, neighbours


def test_neighbours_drops_no_data_and_spaces():
    text = "21602100015, 21602100555, no_data, no_data"
    assert neighbours(text) == ["21602100015", "21602100555"]


def test_main_channel_follows_downstream_links():
    reaches = pd.DataFrame({"reach_id": ["A", "B", "C", "D"],
                            "rch_id_dn": ["B", "C, D", "no_data", "no_data"]})
    assert main_channel(reaches, "A", "C") == ["A", "B", "C"]


def test_main_channel_raises_at_dead_end():
    reaches = pd.DataFrame({"reach_id": ["A", "B"], "rch_id_dn": ["B", "no_data"]})
    with pytest.raises(ValueError):
        main_channel(reaches, "A", "Z")


def series(values: list[float]) -> pd.DataFrame:
    """One reach, one observation every 10 days."""
    dates = pd.date_range("2024-01-01", periods=len(values), freq="10D")
    return pd.DataFrame({"reach_id": "A", "datetime": dates, "wse": values})


def test_spike_is_detected_but_step_is_not():
    spike = spike_size(series([10.0, 10.0, 15.0, 10.0, 10.0]))
    step = spike_size(series([10.0, 10.0, 15.0, 15.0, 15.0]))
    assert spike.max() == 5.0
    assert step.max() == 0.0


def test_flag_checks_marks_values_above_threshold():
    df = pd.DataFrame({"reach_q": [0, 1, 2], "xovr_cal_q": [0, 0, 2], "dark_frac": [0.1, 0.6, 0.0]})
    qc = {"max_reach_q": 1, "max_xovr_cal_q": 1, "max_dark_frac": 0.5}
    assert flag_checks(df, qc).any(axis=1).tolist() == [False, True, True]