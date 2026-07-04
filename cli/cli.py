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

def build_parser():
    parser = argparse.ArgumentParser(description="Inventory management CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_view_all = subparsers.add_parser("view-all", help="View all inventory items")
    p_view_all.set_defaults(func=view_all_items)

    p_view = subparsers.add_parser("view", help="View a single item by ID")
    p_view.add_argument("id", type=int)
    p_view.set_defaults(func=view_specific_item)

    p_add = subparsers.add_parser("add", help="Add a new item manually")
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--brand", required=True)
    p_add.add_argument("--ingredients", default="")
    p_add.add_argument("--barcode", default="")
    p_add.add_argument("--price", type=float, default=0.0)
    p_add.add_argument("--stock", type=int, default=0)
    p_add.set_defaults(func=add_item)

    p_edit = subparsers.add_parser("edit", help="Update one or more fields for an item")
    p_edit.add_argument("id", type=int)
    p_edit.add_argument("--name", default=None)
    p_edit.add_argument("--brand", default=None)
    p_edit.add_argument("--ingredients", default=None)
    p_edit.add_argument("--barcode", default=None)
    p_edit.add_argument("--price", type=float, default=None)
    p_edit.add_argument("--stock", type=int, default=None)
    p_edit.set_defaults(func=edit_item)

    p_delete = subparsers.add_parser("delete", help="Delete an item by ID")
    p_delete.add_argument("id", type=int)
    p_delete.set_defaults(func=delete_item)

    p_lookup = subparsers.add_parser("lookup", help="Find item on OpenFoodFacts and add to inventory")
    p_lookup.add_argument("barcode")
    p_lookup.add_argument("--price", type=float, default=None)
    p_lookup.add_argument("--stock", type=int, default=None)
    p_lookup.set_defaults(func=fetch_and_add)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()    
       