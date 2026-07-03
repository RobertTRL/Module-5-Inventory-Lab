inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "barcode": "0025293001453",
        "ingredients_text": "Filtered water, almonds, cane sugar, sea salt, ...",
        "price": 4.99,
        "stock": 20,
    },
    {
        "id": 2,
        "product_name": "Peanut Butter",
        "brands": "Jif",
        "barcode": "0051500255162",
        "ingredients_text": "Roasted peanuts, sugar, molasses, salt",
        "price": 3.49,
        "stock": 15,
    }
]

next_id = 3

def create_product(product_name, brands, price, ingredients_text="", barcode="", stock_quantity=1):
    global next_id

    item = {
        "id": next_id,
        "product_name": product_name,
        "brands": brands,
        "ingredients_text": ingredients_text,
        "barcode": barcode,
        "price": price,
        "stock_quantity": stock_quantity,
    }

    inventory.append(item)
    next_id += 1
    return item

def create_from_api_data(api_data, price=0.0, stock_quantity=0):

    return create_product(
        product_name=api_data["product_name"],
        brands=api_data["brands"],
        ingredients_text=api_data["ingredients_text"],
        barcode=api_data["barcode"],
        price=price,
        stock_quantity=stock_quantity,
    )