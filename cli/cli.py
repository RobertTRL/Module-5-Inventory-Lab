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