import requests, argparse

BASE_URL = "http://127.0.0.1:5000/inventory"

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