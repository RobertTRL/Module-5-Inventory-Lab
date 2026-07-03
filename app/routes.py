from flask import Blueprint, jsonify, request
from app.data import create_product

inventory_bp = Blueprint("inventory", __name__)

# GET /inventory → Fetch all items
# GET /inventory/<id> → Fetch a single item
# POST /inventory → Add a new item
# PATCH /inventory/<id> → Update an item
# DELETE /inventory/<id> → Remove an item