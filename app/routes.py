from flask import Blueprint, jsonify, request
from app.data import create_product

inventory_bp = Blueprint("inventory", __name__)