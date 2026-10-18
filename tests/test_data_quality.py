
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
    data = pd.read_csv(DATA_FILE)

    # Convert numeric columns to numeric types
    numeric_columns = ["energy_kwh", "voltage_v", "current_a"]
    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="raise")

    # Parse timestamps as timezone-aware UTC values
    data["reading_timestamp"] = pd.to_datetime(
        data["reading_timestamp"], utc=True, errors="raise"
    )

    return data


def test_row_count(df):
    assert len(df) == EXPECTED_READINGS


def test_required_columns(df):
    assert list(df.columns) == REQUIRED_COLUMNS


def test_no_missing_values(df):
    assert not df[REQUIRED_COLUMNS].isna().any().any()
    assert df[REQUIRED_COLUMNS].apply(
        lambda column: column.astype("string").str.strip().eq("").any()
    ).sum() == 0


def test_no_duplicate_readings(df):
    duplicates = df.duplicated(
        subset=["meter_id", "reading_timestamp"]
    )
    assert not duplicates.any()


def test_measurement_ranges(df):
    assert df["energy_kwh"].between(0.1, 8.0).all()
    assert df["voltage_v"].between(215.0, 245.0).all()
    assert df["current_a"].between(0.5, 35.0).all()


def test_timestamps_are_valid_utc(df):
    assert df["reading_timestamp"].notna().all()
    assert str(df["reading_timestamp"].dt.tz) == "UTC"


    


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main(["-v", __file__]))
