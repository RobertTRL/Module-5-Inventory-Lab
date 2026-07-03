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