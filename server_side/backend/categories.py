from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from backend.models import *

categories = Blueprint('categories', __name__)


# ------------------------------
# ✅ Get all categories
# ------------------------------
@categories.route('/service-categories', methods=['GET'])
def get_all_categories():
    all_categories = ServiceCategory.query.all()
    category_list = [{"id": cat.id, "name": cat.name, "picture": cat.picture} for cat in all_categories]
    return jsonify({"categories": category_list, "total": len(category_list)}), 200


# ------------------------------
# ✅ Add new category
# ------------------------------
@categories.route('/service-categories', methods=['POST'])
@jwt_required()
def add_service_category():
    claims = get_jwt()
    if claims.get("role") != 2:
        return jsonify({"error": "Admins only!"}), 403

    data = request.json
    if not data.get("name"):
        return jsonify({"error": "Category name is required"}), 400

    if ServiceCategory.query.filter_by(name=data["name"]).first():
        print("Category already exists...")
        return jsonify({"error": "Category already exists"}), 400

    new_category = ServiceCategory(
        name=data["name"],
        picture=data.get("picture")  # Optional picture URL
    )
    
    db.session.add(new_category)
    db.session.commit()
    
    return jsonify({"message": "Service category added successfully", "id": new_category.id}), 201


# ------------------------------
# ✅ Get a single category
# ------------------------------
@categories.route('/service-categories/<int:id>', methods=['GET'])
def get_category(id):
    category = ServiceCategory.query.get(id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    return jsonify({"id": category.id, "name": category.name, "picture": category.picture}), 200


# ------------------------------
# ✅ Edit a category
# ------------------------------
@categories.route('/service-categories/<int:id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    claims = get_jwt()
    if claims.get("role") != 2:
        return jsonify({"error": "Admins only!"}), 403

    category = ServiceCategory.query.get(id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    data = request.json
    if not data.get("name"):
        return jsonify({"error": "Category name is required"}), 400

    if ServiceCategory.query.filter(ServiceCategory.name == data["name"], ServiceCategory.id != id).first():
        return jsonify({"error": "Category with this name already exists"}), 400

    category.name = data["name"]
    category.picture = data.get("picture", category.picture)  # Update if provided

    db.session.commit()

    return jsonify({"message": "Service category updated successfully"}), 200


# ------------------------------
# ✅ Delete a category
# ------------------------------
@categories.route('/service-categories/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    claims = get_jwt()
    if claims.get("role") != 2:
        return jsonify({"error": "Admins only!"}), 403

    category = ServiceCategory.query.get(id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": "Service category deleted successfully"}), 200
