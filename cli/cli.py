import requests, argparse

BASE_URL = "http://127.0.0.1:5000/inventory"

# Print item -> prints relevent fields for an item
# Handle request -> handles various requests, takes request and url as args
# view all items -> retrieves all data from inventory
# view specific item -> retrieves data with the id specified
# add item -> adds a new item
# edit item -> edits an already existing item with the fields specified
# delete item -> deletes an already existing item with the id specified
# lookup and add -> retrieves an item from the external api using a barcode, adds it to the inventory

def print_item(item):
    print(f"\nID: {item['id']}")
    print(f"  Name:        {item['product_name']}")
    print(f"  Brand:       {item.get('brands', 'N/A')}")
    print(f"  Barcode:     {item.get('barcode', 'N/A')}")
    print(f"  Price:       ${item.get('price', 0):.2f}")
    print(f"  Stock:       {item.get('stock_quantity', 0)}")
    print(f"  Ingredients: {item.get('ingredients_text', 'N/A')}")

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
    
    for item in items:
        print_item(item)

def view_specific_item(args):
    response = handle_request("GET", f"{BASE_URL}/{args.id}")

    if not response:
        print("Request has failed!")
        return

    print_item(response.json())

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
    print_item(response.json())
           