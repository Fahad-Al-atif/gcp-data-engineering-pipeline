
from pathlib import Path

import pandas as pd
import pytest

DATA_FILE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "sample"
    / "meter_readings.csv"
)

EXPECTED_READINGS = 25_000
EXPECTED_DEFECTS_PER_TYPE = 100

REQUIRED_COLUMNS = [
    "meter_id",
    "reading_timestamp",
    "energy_kwh",
    "voltage_v",
    "current_a",
    "source_system",
]


@pytest.fixture(scope="module")
def df():
    return pd.read_csv(DATA_FILE)


@pytest.fixture(scope="module")
def prepared(df):
    data = df.copy()

    data["reading_timestamp_parsed"] = pd.to_datetime(
        data["reading_timestamp"],
        utc=True,
        errors="coerce",
    )

    for column in ["energy_kwh", "voltage_v", "current_a"]:
        data[f"{column}_parsed"] = pd.to_numeric(
            data[column],
            errors="coerce",
        )

    return data


def test_row_count(df):
    assert len(df) == EXPECTED_READINGS


def test_required_columns(df):
    assert list(df.columns) == REQUIRED_COLUMNS


def test_missing_meter_ids(df):
    missing = (
        df["meter_id"].isna()
        | df["meter_id"].astype("string").str.strip().eq("")
    )
    assert missing.sum() == EXPECTED_DEFECTS_PER_TYPE


def test_invalid_numeric_values(prepared):
    invalid = prepared["energy_kwh_parsed"].isna()
    assert invalid.sum() == EXPECTED_DEFECTS_PER_TYPE


def test_out_of_range_voltage(prepared):
    invalid = ~prepared["voltage_v_parsed"].between(215.0, 245.0)
    assert invalid.sum() == EXPECTED_DEFECTS_PER_TYPE


def test_invalid_timestamps(prepared):
    invalid = prepared["reading_timestamp_parsed"].isna()
    assert invalid.sum() == EXPECTED_DEFECTS_PER_TYPE


def test_duplicate_readings(prepared):
    valid_keys = prepared[
        prepared["meter_id"].notna()
        & prepared["meter_id"].astype("string").str.strip().ne("")
        & prepared["reading_timestamp_parsed"].notna()
    ]

    duplicates = valid_keys.duplicated(
        subset=["meter_id", "reading_timestamp_parsed"],
        keep="first",
    )

    assert duplicates.sum() == EXPECTED_DEFECTS_PER_TYPE


if __name__ == "__main__":
    raise SystemExit(pytest.main(["-v", __file__]))
