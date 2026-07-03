from flask import Blueprint, jsonify, request
from app import data

inventory_bp = Blueprint("inventory", __name__)

# GET /inventory → Fetch all items
# GET /inventory/<id> → Fetch a single item
# POST /inventory → Add a new item
# PATCH /inventory/<id> → Update an item
# DELETE /inventory/<id> → Remove an item

@inventory_bp.route("/", methods=["GET"])
def get_all_items():
    return jsonify(data.inventory), 200

@inventory_bp.route("/<int:item_id>", methods=["GET"])
def get_item_by_id(item_id):
    item = next((i for i in data.inventory if i.id == item_id), None)

    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    return jsonify(item), 200

@inventory_bp.route("/", methods=["POST"])
def create_item():
    body_data = request.get_json()

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

@inventory_bp.route("/<int:item_id>", methods=["PATCH"])
