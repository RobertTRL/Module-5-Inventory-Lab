import requests, argparse

BASE_URL = "http://127.0.0.1:5000/inventory"

# Handle request -> handles various requests, takes request and url as args
# view all items -> retrieves all data from inventory
# view specific item -> retrieves data with the id specified
# add item -> adds a new item
# edit item -> edits an already existing item with the fields specified
# delete item -> deletes an already existing item with the id specified
# fetch and add -> retrieves an item from the external api using a barcode, adds it to the inventory

def handle_request(method, url, **kwargs):
    try:
        response = requests.request(method, url, timeout=5, **kwargs)
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to server: {e}")
        return None

    if response.status_code == 404:
        print("Not found.")
        return None
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Server error: {e}")
        return None

    return response

def view_all_items(args):
    response = handle_request("GET", BASE_URL)

    if not response:
        print("Request has failed!")
        return
    
    items = response.json()

    if not items:
        print("Inventory is empty")
        return
    
    print(items)

def view_specific_item(args):
    response = handle_request("GET", f"{BASE_URL}/{args.id}")

    if not response:
        print("Request has failed!")
        return

    print(response.json())

def add_item(args):
    payload = {
        "product_name": args.name,
        "brands": args.brand,
        "ingredients_text": args.ingredients or "",
        "barcode": args.barcode or "",
        "price": args.price,
        "stock_quantity": args.stock,
    }

    response = handle_request("POST", BASE_URL, json=payload)

    if not response:
        print("Request has failed!")
        return
    
    print("Item added:")
    print(response.json())

def edit_item(args):
    field_map = {
        "name": "product_name",
        "brand": "brands",
        "ingredients": "ingredients_text",
        "barcode": "barcode",
        "price": "price",
        "stock": "stock_quantity",
    }

    payload = {
        api_field: getattr(args, cli_field)
        for cli_field, api_field in field_map.items()
        if getattr(args, cli_field) is not None
    }

    if not payload:
        print("Provide at least one field to update (--name, --brand, --ingredients, --barcode, --price, --stock).")
        return

    response = handle_request("PATCH", f"{BASE_URL}/{args.id}", json=payload)
    if not response:
        print("Request has failed!")
        return
    
    print("Item updated:")
    print(response.json())

def delete_item(args):
    response = handle_request("DELETE", f"{BASE_URL}/{args.id}")

    if not response:
        print("Request has failed!")
        return
    
    print("Item deleted:")
    print(response.json())

def fetch_and_add(args):
    payload = {}
    if args.price is not None:
        payload["price"] = args.price
    if args.stock is not None:
        payload["stock_quantity"] = args.stock

    response = handle_request("POST", f"{BASE_URL}/lookup/{args.barcode}", json=payload)

    if not response:
        print("Request has failed!")
        return

    print("Item added from OpenFoodFacts:")
    print(response.json())
       