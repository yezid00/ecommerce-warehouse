
# ecommerce-warehouse

A small data-engineering demo project that demonstrates generating sample ecommerce data, creating a simple warehouse/schema, running analytics, and producing a report.

## Contents

- `setup_warehouse.py` - Prepare any warehouse infrastructure or local database objects used by the project.
- `create_schema.py` - Create the database schema / tables used by the warehouse.
- `generate_data.py` - Produce sample data (customers, orders, products, etc.) for ingestion.
- `db_connection.py` - Database connection helper. Update this file or set environment variables to point to your database.
- `analytics.py` - Run analytics queries against the warehouse and output results.
- `generate_report.py` - Build a report from analytics output (the current file you're editing).
- `requirements.txt` - Python dependencies for the project.

## Prerequisites

- Python 3.8+ installed
- A database (SQLite, Postgres, etc.) accessible from this project OR adjust the code to use a local SQLite file.

Note: This repository ships a `db_connection.py` helper. Configure the connection string there, or update it to read from environment variables (for example `DATABASE_URL`).

## Setup

1. (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate    # on Windows with bash.exe
# or: source .venv/bin/activate  # on Unix-like systems
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your database connection in `db_connection.py` (or set the env var used by the project). If you prefer SQLite for quick local runs, update `db_connection.py` to point to a local `.db` file.

## Typical usage

Run the scripts in this order for a full local end-to-end run:

```bash
python setup_warehouse.py    # prepare infrastructure (if needed)
python create_schema.py     # create database tables/schema
python generate_data.py     # populate sample data
python analytics.py         # run analytics queries
python generate_report.py   # produce the final report (CSV/console)
```

Replace `python` with the full interpreter path if your environment requires it (for example, `python3`).

## Files of interest

- `db_connection.py`: central place for DB config. If you are running against Postgres, set a connection string there. For a quick demo run, you can point it to `sqlite:///warehouse.db` or a local file-based DB.
- `generate_data.py`: small data generator — tweak data volumes or schemas here.
- `generate_report.py`: current entry-point for creating the report. Inspect and modify filters or output formats as needed.

## Troubleshooting

- If a script can't connect to the DB, confirm the connection settings in `db_connection.py` and that the target DB is reachable.
- If dependencies fail to install, ensure your pip is up to date: `pip install -U pip` and retry.

## Next steps / Improvements

- Add a small integration test that runs the end-to-end flow against an in-memory or temporary database.
- Add a `config.example.env` and have `db_connection.py` read from `DATABASE_URL` for easier deployment.

## License

This project is provided as-is. Add a license file (e.g. MIT) if you intend to publish or share.

## Contact

For questions about this repository, open an issue or contact the maintainer.
