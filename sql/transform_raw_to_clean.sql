
-- Transform raw smart meter readings into the clean layer.
-- The raw table remains unchanged.

CREATE OR REPLACE TABLE
  `de-gcp-pipeline-lab.clean.meter_readings` AS

WITH prepared AS (
  SELECT
    TRIM(meter_id) AS meter_id,
    SAFE_CAST(reading_timestamp AS TIMESTAMP) AS reading_timestamp,
    SAFE_CAST(energy_kwh AS FLOAT64) AS energy_kwh,
    SAFE_CAST(voltage_v AS FLOAT64) AS voltage_v,
    SAFE_CAST(current_a AS FLOAT64) AS current_a,
    TRIM(source_system) AS source_system
  FROM `de-gcp-pipeline-lab.raw.meter_readings`
),

valid_readings AS (
  SELECT *
  FROM prepared
  WHERE
    meter_id IS NOT NULL
    AND meter_id != ''
    AND reading_timestamp IS NOT NULL
    AND energy_kwh BETWEEN 0.1 AND 8.0
    AND voltage_v BETWEEN 215.0 AND 245.0
    AND current_a BETWEEN 0.5 AND 35.0
    AND source_system IS NOT NULL
    AND source_system != ''
),

deduplicated AS (
  SELECT *
  FROM valid_readings
  QUALIFY ROW_NUMBER() OVER (
    PARTITION BY meter_id, reading_timestamp
    ORDER BY meter_id
  ) = 1
)

SELECT *
FROM deduplicated;
