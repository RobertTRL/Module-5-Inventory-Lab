import requests

BASE_URL = "https://world.openfoodfacts.org/api/v3/product"
SEARCH_URL = "https://world.openfoodfacts.org/cgi/search.pl"

def fetch_by_barcode(barcode):

    url = f"{BASE_URL}/{barcode}.json"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error contacting OpenFoodFacts: {e}")
        return None

    data = response.json()

    if data.get("status") != 1:
        return None

    product = data.get("product", {})
    return {
        "product_name": product.get("product_name", "Unknown"),
        "brands": product.get("brands", "Unknown"),
        "ingredients_text": product.get("ingredients_text", ""),
        "barcode": barcode,
    }