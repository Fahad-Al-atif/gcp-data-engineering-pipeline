
-- Validate the BigQuery clean layer.
-- Each check should return PASS.

WITH metrics AS (
  SELECT
    COUNT(*) AS total_rows,
    COUNTIF(
      meter_id IS NULL OR TRIM(meter_id) = ''
    ) AS invalid_meter_ids,
    COUNTIF(reading_timestamp IS NULL) AS invalid_timestamps,
    COUNTIF(
      energy_kwh IS NULL
      OR energy_kwh NOT BETWEEN 0.1 AND 8.0
    ) AS invalid_energy,
    COUNTIF(
      voltage_v IS NULL
      OR voltage_v NOT BETWEEN 215.0 AND 245.0
    ) AS invalid_voltage,
    COUNTIF(
      current_a IS NULL
      OR current_a NOT BETWEEN 0.5 AND 35.0
    ) AS invalid_current,
    COUNTIF(
      source_system IS NULL OR TRIM(source_system) = ''
    ) AS invalid_source_system
  FROM `de-gcp-pipeline-lab.clean.meter_readings`
),

duplicate_metrics AS (
  SELECT COUNT(*) AS duplicate_readings
  FROM (
    SELECT meter_id, reading_timestamp
    FROM `de-gcp-pipeline-lab.clean.meter_readings`
    GROUP BY meter_id, reading_timestamp
    HAVING COUNT(*) > 1
  )
),

all_metrics AS (
  SELECT *
  FROM metrics
  CROSS JOIN duplicate_metrics
)

SELECT
  test_name,
  observed_value,
  expected_value,
  IF(observed_value = expected_value, 'PASS', 'FAIL') AS result
FROM all_metrics
CROSS JOIN UNNEST([
  STRUCT('Expected row count' AS test_name, total_rows AS observed_value, 25000 AS expected_value),
  STRUCT('Invalid meter IDs', invalid_meter_ids, 0),
  STRUCT('Invalid timestamps', invalid_timestamps, 0),
  STRUCT('Invalid energy values', invalid_energy, 0),
  STRUCT('Invalid voltage values', invalid_voltage, 0),
  STRUCT('Invalid current values', invalid_current, 0),
  STRUCT('Invalid source systems', invalid_source_system, 0),
  STRUCT('Duplicate readings', duplicate_readings, 0)
]);
