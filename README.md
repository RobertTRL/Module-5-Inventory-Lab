# Inventory Management System

A Flask REST API with a CLI frontend for managing a food product inventory. Product data can be added manually or fetched automatically from the [OpenFoodFacts](https://world.openfoodfacts.org/) API using a barcode.

## Project Structure

```
inventory-api/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── data.py               # In-memory inventory store
│   ├── routes.py              # API endpoints (blueprint)
│   └── openfoodfacts.py       # OpenFoodFacts API integration
├── cli/
│   └── cli.py                 # Argparse-based CLI frontend
├── tests/
│   ├── conftest.py
│   ├── test_routes.py
│   ├── test_openfoodfacts.py
│   └── test_cli.py
├── run.py                     # Flask entry point
├── requirements.txt
└── README.md
```

## Setup

**1. Clone the repo**

```bash
git clone <your-repo-url>
cd inventory-api
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv

# Windows (cmd)
venv\Scripts\activate

# macOS / Linux / WSL
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist yet or is out of date:

```bash
pip install flask requests pytest
pip freeze > requirements.txt
```

## Running the API

Start the Flask server from the project root:

```bash
python run.py
```

The API will run at `http://127.0.0.1:5000` with debug mode enabled. Keep this running in its own terminal — the CLI talks to it over HTTP.

## API Endpoints

| Method | Route | Description |
|---|---|---|
| GET | `/inventory` | Fetch all items |
| GET | `/inventory/<id>` | Fetch a single item |
| POST | `/inventory` | Add a new item manually |
| POST | `/inventory/lookup/<barcode>` | Look up a product on OpenFoodFacts and add it |
| PATCH | `/inventory/<id>` | Update one or more fields on an item |
| DELETE | `/inventory/<id>` | Remove an item |

## Using the CLI

With the Flask server running, open a **second terminal**, activate the same venv, and run CLI commands from the project root:

```bash
python cli/cli.py <command> [options]
```

### Commands

**View all items**
```bash
python cli/cli.py view-all
```

**View one item by ID**
```bash
python cli/cli.py view 1
```

**Add an item manually**
```bash
python cli/cli.py add --name "Oat Milk" --brand Oatly --price 3.99 --stock 10
```
Optional flags: `--ingredients`, `--barcode`

**Add an item via OpenFoodFacts barcode lookup**
```bash
python cli/cli.py lookup 3017620422003 --price 5.99 --stock 8
```
`--price` and `--stock` are optional here and default to `0` if omitted.

**Update an item** (only pass the fields you want to change)
```bash
python cli/cli.py edit 1 --price 5.49 --stock 12
python cli/cli.py edit 1 --brand "Silk Organic"
```
Available fields: `--name`, `--brand`, `--ingredients`, `--barcode`, `--price`, `--stock`

**Delete an item**
```bash
python cli/cli.py delete 2
```

**Help for any command**
```bash
python cli/cli.py <command> --help
```

## Running Tests

Tests use `pytest` and `unittest.mock` to simulate API responses — no real network calls or running Flask server are required.

From the project root:

```bash
pytest -v
```

Test coverage includes:
- `test_routes.py` — all API endpoints (GET, POST, PATCH, DELETE), including 404/400 edge cases
- `test_openfoodfacts.py` — the OpenFoodFacts integration, with mocked HTTP responses for found/not-found/error cases
- `test_cli.py` — CLI commands, with mocked HTTP requests to the API

## Notes

- Inventory data is stored **in memory** — it resets every time the Flask server restarts.
- Debug mode (`app.run(debug=True)`) is enabled in `run.py` for development; disable it before any production use.

## Author

**RobertTRL** - [github.com/RobertTRL](https://github.com/RobertTRL)