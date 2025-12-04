# OECD Electricity ETL & Analytics Dashboard  
Digital Futures – Data Engineering Capstone Project

This project delivers a complete end-to-end ETL pipeline and interactive Streamlit dashboard using publicly available electricity production and trade datasets from the International Energy Agency (IEA).

The capstone focuses primarily on demonstrating applied data engineering practices, including data ingestion, transformation, validation, testing, orchestration, and visualisation successfully carried through from raw data to a final analytical product.

Approximately 70% of the project is engineering-focused, with the remaining 30% dedicated to analytical presentation and communication.

------------------------------------------------------------

## Project Overview

This pipeline processes monthly electricity production and trade data from January 2015 to December 2025 for 38 OECD countries.

Key project objectives:

- Build a fully modular ETL pipeline using Python and Pandas
- Standardise and enrich energy datasets for analytical use
- Implement data quality validation with automated unit testing
- Create a reproducible orchestration workflow to generate final outputs
- Build a multi-page Streamlit dashboard to demonstrate analytical storytelling

------------------------------------------------------------

## Data Source

- International Energy Agency (IEA)
- Public CSV downloads
- Monthly electricity:
  - Production by fuel source
  - Electricity import/export trade
- Raw datasets combined exceed 330,000 records

The dataset is filtered to OECD member countries to ensure geographic and regulatory comparability.

------------------------------------------------------------

## Technology Stack

Programming Language  
- Python 3.11+

Data Processing  
- Pandas

Testing  
- Pytest

Visualisation  
- Plotly

Dashboard  
- Streamlit

Logging  
- Python logging framework

Environment  
- Virtual environments (venv)

Version Control  
- Git and GitHub

------------------------------------------------------------

## Folder Structure

.gitignore
README.md

config/
- config.toml           Global configuration settings
- paths_config.py      Centralised file-path definitions

data/
- raw/                 Original IEA source CSV files
- processed/           Final analytics-ready dataset (oecd_energy_fact.csv)
- output/              Generated dimensional models and star-schema tables
  - dim_country.csv
  - dim_date.csv
  - fact_electricity_production_monthly.csv
  - fact_electricity_production_star.csv
  - fact_electricity_trade_monthly.csv
  - fact_electricity_trade_star.csv

logs/
- capstone_app.log     Application and pipeline runtime logs

scripts/
- build_dim_country.py       Builds country dimension tables
- build_dim_date.py          Builds date dimension tables
- build_processed_oecd_dataset.py  Produces the final processed OECD dataset
- build_star_schema.py      Builds star-schema fact tables
- explore_categories.py    Exploratory data analysis and category inspection
- run_pipeline.py           ETL orchestration runner (extract → transform → load)
- run_quality_checks.py    Executes additional data validation checks

src/
- capstone_etl/
  - extract/          Dataset ingestion logic
  - transform/       Cleaning, standardisation, feature engineering, aggregation
  - load/             Dataset persistence logic
  - quality/          Data quality and reconciliation checks
  - analytics/        KPI computation, backend loaders, and logging utilities
  - utils/            Shared helpers (including structured logging)

streamlit/
- 1_Capstone_Overview.py     Landing and project overview page
- pages/
  - 2_ETL_Pipeline.py       ETL workflow walkthrough
  - 3_Visualisations.py    Interactive KPI dashboards
  - 4_Whats_Next.py         Personal reflection and future roadmap
- assets/                   Images used across dashboard pages
- config.toml               Streamlit application configuration

tests/
- test_oecd_pipeline.py    End-to-end pipeline validation tests
- test_transform.py        Unit tests for transformation logic

Other Files
- requirements.txt         Python dependency definitions
- pyproject.toml           Build and packaging configuration
- project_diagnosis_summary.txt  Internal project notes and diagnostics
- print_tree.py            Repo structure diagnostic script


------------------------------------------------------------

## Pipeline Architecture

The project follows a modular ETL design:

Raw CSV Files  
↓  
[Extraction]  
↓  
[Transformation]  
↓  
[Aggregation & Feature Engineering]  
↓  
[Load — Processed CSV]  
↓  
[Analytics & Visualisation]
↓  
[Streamlit Dashboard]

------------------------------------------------------------

## ETL Stages

Extraction

- Loads raw IEA CSV datasets
- Applies geographic filters (OECD only)
- Normalises schema structure across datasets

Transformation

- Cleans data and corrects inconsistent types or formats
- Standardises naming conventions
- Creates engineered features including:
  - fuel_group classifications (LOW_CARBON / NUCLEAR / FOSSIL)
  - validation and atomic-fuel flags
- Aggregates monthly metrics
- Calculates KPIs including energy share percentages, import dependency, and grid losses

Load

- Persists the final processed dataframe to:

data/processed/oecd_energy_fact.csv

This dataset is used as the source for all dashboard visualisations.

------------------------------------------------------------

## Pipeline Orchestration

The project includes a pipeline runner:

run_pipeline.py

This script controls execution of the full ETL workflow by:

- Calling the extract, transform, and load phases sequentially
- Logging the start and completion of each phase
- Capturing failure states with exception logging
- Producing the final analytics dataset used by the dashboard

This orchestration pattern reflects common production batch pipeline design.

------------------------------------------------------------

## Local Setup

Clone the repository and navigate into the project directory.

Create and activate a virtual environment.

Install dependencies from requirements.txt.

------------------------------------------------------------

## Run the ETL Pipeline

Execute:

python run_pipeline.py

Successful execution generates:

data/processed/oecd_energy_fact.csv

------------------------------------------------------------

## Testing

Unit tests validate the happy-path behaviour of critical ETL components including:

- Data cleaning utilities
- Feature engineering logic
- Configuration and environment validation
- Logging helpers

Run all tests with:

pytest

------------------------------------------------------------

## Streamlit Dashboard

After running the pipeline, launch the dashboard with:

streamlit run streamlit/app.py

Dashboard features include:

- Country selection and comparison filtering
- Year-range sliders
- Interactive analytical views:
  - Energy mix distribution
  - Renewable trend comparisons
  - Import dependency analysis
  - Grid loss visualisation

Custom CSS styling has been applied for a consistent dark corporate theme.

------------------------------------------------------------

## Data Validation and Known Limitations

Automated validation and reconciliation tests are applied throughout the pipeline.

One reconciliation test comparing IEA published totals to calculated totals remains intentionally unresolved due to known data inconsistencies within the source datasets. This limitation is documented transparently rather than suppressed or artificially adjusted.

------------------------------------------------------------

## Project Planning

Delivery was managed through Agile-style planning practices including:

- Definition of epics and user stories
- Kanban task tracking on the repo's Github Project tab
- Iterative development and refactoring with test-first principles

The project emphasis remained on establishing a complete functioning pipeline before expanding analytical features or presentation polish.

------------------------------------------------------------

## Personal Learning and Next Steps

Future development pathways identified from this capstone include:

- Expanding automated testing around reconciliation scenarios, edge-case handling, and broader data quality coverage.
- Extending orchestration capability beyond the current run_pipeline.py design toward schedulers and workflow managers such as Airflow or AWS Step Functions.
- Migrating pipelines into cloud environments using infrastructure-as-code.
- Refining dashboard UX through advanced layout composition and prototyping tools.
- Building additional end-to-end data engineering projects to strengthen portfolio depth.

------------------------------------------------------------

## Capstone project by:

Sailesh Vyas  
Digital Futures – Data Engineering Academy

This project demonstrates applied capability across data pipeline engineering, validation testing, workflow orchestration, and analytical presentation.


