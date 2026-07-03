from flask import Blueprint, jsonify, request
from app import data

inventory_bp = Blueprint("inventory", __name__)

# GET /inventory → Fetch all items
# GET /inventory/<id> → Fetch a single item
# POST /inventory → Add a new item
# PATCH /inventory/<id> → Update an item
# DELETE /inventory/<id> → Remove an item

@inventory_bp.route("/", methods=["GET"]):
def get_all_items():
    return jsonify(inventory), 200