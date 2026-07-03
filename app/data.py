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

def create_product(product_name, brands, ingredients_text="", barcode="", price=0.0, stock_quantity=0):
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