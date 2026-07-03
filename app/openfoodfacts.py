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

def search_by_name(name, limit=5):

    params = {
        "search_terms": name,
        "json": 1,
        "page_size": limit,
    }

    try:
        response = requests.get(SEARCH_URL, params=params, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error contacting OpenFoodFacts: {e}")
        return []

    data = response.json()
    products = data.get("products", [])

    results = []
    for product in products:
        results.append({
            "product_name": product.get("product_name", "Unknown"),
            "brands": product.get("brands", "Unknown"),
            "ingredients_text": product.get("ingredients_text", ""),
            "barcode": product.get("code", ""),
        })
    return results