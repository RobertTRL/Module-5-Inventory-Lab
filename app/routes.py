from flask import Blueprint, jsonify, request
from app import data, openfoodfacts

inventory_bp = Blueprint("inventory", __name__)

# GET /inventory → Fetch all items
# GET /inventory/<id> → Fetch a single item
# POST /inventory → Add a new item
# POST /inventory/<barcode> → Retrieves the item with the barcode and adds it
# PATCH /inventory/<id> → Update an item
# DELETE /inventory/<id> → Remove an item

@inventory_bp.route("", methods=["GET"])
def get_all_items():
    return jsonify(data.inventory), 200

@inventory_bp.route("/<int:item_id>", methods=["GET"])
def get_item_by_id(item_id):
    item = next((i for i in data.inventory if i["id"] == item_id), None)

    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    return jsonify(item), 200

@inventory_bp.route("", methods=["POST"])
def create_item():
    body_data = request.get_json(silent=True)

    if not body_data or "product_name" not in body_data or "brands" not in body_data or "price" not in body_data:
        return jsonify({"error": "product_name, brands and/or price are required"}), 400
    
    payload = data.create_product(
        product_name=body_data["product_name"],
        brands=body_data["brands"],
        price=body_data["price"],
        ingredients_text=body_data.get("ingredients_text", ""),
        barcode=body_data.get("barcode", ""),
        stock_quantity=body_data.get("stock_quantity", 1),
    )

    return jsonify(payload), 201

@inventory_bp.route("/lookup/<barcode>", methods=["POST"])
def lookup_and_add(barcode):
    api_data = openfoodfacts.fetch_by_barcode(barcode)
    if api_data is None:
        return jsonify({"error": "Product not found on OpenFoodFacts"}), 404

    body = request.get_json(silent=True) or {}
    item = data.create_from_api_data(
        api_data,
        price=body.get("price", 0.0),
        stock_quantity=body.get("stock_quantity", 0),
    )
    
    return jsonify(item), 201    

@inventory_bp.route("/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = next((i for i in data.inventory if i["id"] == item_id), None)

    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    body_data = request.get_json(silent=True)

    if not body_data:
        return jsonify({"error": "No data provided"}), 400
    
    allowed_fields = ["product_name", "brands", "price", "ingredients_text", "barcode", "stock_quantity"]

    for field in allowed_fields:
        if field in body_data:
            item[field] = body_data[field]
    
    return jsonify(item), 200

@inventory_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item_index = next((i for i, item in enumerate(data.inventory) if item["id"] == item_id), None)

    if item_index is None:
        return jsonify({"error": "Item not found"}), 404
    
    deleted_item = data.inventory.pop(item_index)
    return jsonify(deleted_item), 200
