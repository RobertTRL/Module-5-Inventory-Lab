inventory-api/
├── app/
│   ├── __init__.py          # create_app() factory, registers blueprint
│   ├── data.py               # in-memory inventory array + ID counter
│   ├── routes.py             # blueprint: all /inventory endpoints
│   └── openfoodfacts.py      # external API wrapper functions
├── cli/
│   └── cli.py                 # CLI frontend, talks to the Flask API over HTTP
├── tests/
│   ├── test_routes.py
│   ├── test_cli.py
│   └── test_openfoodfacts.py
├── run.py                     # entry point, app.run(debug=True)
├── requirements.txt
├── .gitignore
└── README.md