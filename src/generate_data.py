
import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Project configuration
NUM_READINGS = 25000
NUM_METERS = 100
OUTPUT_FILE = Path("data/sample/meter_readings.csv")

random.seed(42)

# Ensure the output directory exists
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

start_time = datetime(2026, 10, 1, tzinfo=timezone.utc)

fieldnames = [
    "meter_id",
    "reading_timestamp",
    "energy_kwh",
    "voltage_v",
    "current_a",
    "source_system",
]

with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(NUM_READINGS):
        meter_number = (i % NUM_METERS) + 1
        timestamp = start_time + timedelta(minutes=30 * i)

        writer.writerow({
            "meter_id": f"MTR-{meter_number:04d}",
            "reading_timestamp": timestamp.isoformat(),
            "energy_kwh": round(random.uniform(0.1, 8.0), 3),
            "voltage_v": round(random.uniform(215.0, 245.0), 2),
            "current_a": round(random.uniform(0.5, 35.0), 2),
            "source_system": "synthetic_meter_system",
        })

print(f"Generated {NUM_READINGS} readings: {OUTPUT_FILE}")
