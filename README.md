# Cloud-Native Data Engineering Pipeline

A portfolio project demonstrating an end-to-end data engineering pipeline using Google Cloud Platform (GCP), Python, SQL, Cloud Storage, and BigQuery.

## Project Overview

This project simulates a smart meter data pipeline using synthetic electricity readings. It demonstrates data generation, cloud storage, ingestion into BigQuery, SQL transformations, and automated data quality testing.

## Architecture

```text
Python Synthetic Data Generator
              |
              v
       Google Cloud Storage
              |
              v
       BigQuery - Raw
              |
              v
     SQL Transformations
              |
              v
       BigQuery - Clean
              |
              v
      Analytics-Ready Tables
```

## Technologies

- **Python:** Synthetic data generation.
- **Pandas:** Data validation and inspection.
- **Pytest:** Automated data quality tests.
- **Google Cloud Storage:** Storage for the source CSV file.
- **BigQuery:** Cloud data warehouse and SQL transformations.
- **Git and GitHub:** Version control and project documentation.

## Data

The pipeline uses a synthetic dataset containing 25,000 smart meter readings across 100 meters.

Each reading includes:

- `meter_id`
- `reading_timestamp`
- `energy_kwh`
- `voltage_v`
- `current_a`
- `source_system`

No confidential company data is used.

## Data Quality

Automated Python tests validate:

- Expected row count.
- Required columns.
- Missing and blank values.
- Duplicate meter readings.
- Measurement ranges.
- Valid UTC timestamps.

**Python test results:** 6 tests passed.

Additional SQL checks were performed in BigQuery to validate row counts, unique readings, and measurement ranges.

## BigQuery Data Layers

- **Raw:** Stores the ingested source data.
- **Clean:** Stores transformed data after applying validation rules.

The raw layer is preserved separately from the clean layer.

## Cost Management

This project is designed to minimize cloud costs. Cloud resources are created only when needed, and billing budgets and alerts are used to monitor spending.

Budget alerts do not automatically stop resource usage.

## Data Privacy

Only synthetic data is used. No confidential company data, credentials, or secrets should be committed to the repository.

## Project Status

Core ingestion and initial data quality validation are complete. Further development will focus on reproducible transformations, analytics-ready tables, and improved pipeline orchestration.
