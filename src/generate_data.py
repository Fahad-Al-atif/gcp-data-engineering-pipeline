
import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Project configuration
NUM_READINGS = 25_000
NUM_METERS = 100
FAULTS_PER_TYPE = 100

OUTPUT_FILE = Path("data/sample/meter_readings.csv")
random.seed(42)
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
start_time = datetime(2026, 10, 1, tzinfo=timezone.utc)

fieldnames = [  "meter_id","reading_timestamp", "energy_kwh",  "voltage_v","current_a","source_system",]
    
    

# Generate the original readings.
rows = []

for i in range(NUM_READINGS):
    meter_number = (i % NUM_METERS) + 1
    timestamp = start_time + timedelta(minutes=30 * i)

    rows.append({
        "meter_id": f"MTR-{meter_number:04d}",
        "reading_timestamp": timestamp.isoformat(),
        "energy_kwh": round(random.uniform(0.1, 8.0), 3),
        "voltage_v": round(random.uniform(215.0, 245.0), 2),
        "current_a": round(random.uniform(0.5, 35.0), 2),
        "source_system": "synthetic_meter_system",
    })

# Inject controlled defects into separate rows.
n = FAULTS_PER_TYPE

# 1. Missing meter IDs
for i in range(0, n):
    rows[i]["meter_id"] = ""

# 2. Invalid numeric values
for i in range(n, 2 * n):
    rows[i]["energy_kwh"] = "not_a_number"

# 3. Measurements outside the allowed range
for i in range(2 * n, 3 * n):
    rows[i]["voltage_v"] = 500.0

# 4. Invalid timestamps
for i in range(3 * n, 4 * n):
    rows[i]["reading_timestamp"] = "INVALID_TIMESTAMP"

# 5. Duplicate meter/timestamp pairs.
# Copy keys from valid rows 500-599 into the final 100 rows.
for offset in range(n):
    target_index = NUM_READINGS - n + offset
    source_index = 5 * n + offset

    rows[target_index]["meter_id"] = rows[source_index]["meter_id"]
    rows[target_index]["reading_timestamp"] = (
        rows[source_index]["reading_timestamp"]
    )

# Write the dataset.
with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} readings: {OUTPUT_FILE}")
print("Injected defects:")
print(f"- Missing meter IDs: {n}")
print(f"- Invalid numeric values: {n}")
print(f"- Out-of-range voltage values: {n}")
print(f"- Invalid timestamps: {n}")
print(f"- Duplicate meter/timestamp pairs: {n}")
