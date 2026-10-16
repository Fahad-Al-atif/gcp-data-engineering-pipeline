# Cloud-Native Data Engineering Pipeline

A portfolio project demonstrating a cloud-native data pipeline using
Google Cloud Platform, Python, SQL, Cloud Storage, and BigQuery.

## Project Goals

- Ingest synthetic data into Google Cloud Storage.
- Load raw data into BigQuery.
- Validate and transform data using SQL.
- Build analytics-ready tables.
- Test data quality and document the pipeline.

## Architecture

Synthetic Data -> Cloud Storage -> BigQuery Raw -> Data Quality
-> BigQuery Clean -> Analytics Tables

## Cost Management

This project is designed to minimize cloud costs.
Cloud resources will only be created when needed and monitored
through Google Cloud Billing budgets and alerts.

## Data Privacy

Only synthetic or publicly available data will be used.
No confidential company data or credentials will be committed.

## Status

Environment setup in progress.
