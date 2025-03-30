from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from backend.models import db, Service, ServiceCategory, ServiceRequest
from backend.cache import cache

services = Blueprint('services', __name__)

# ------------------------------
# ✅ Get All Services
# ------------------------------
@services.route('/services', methods=['GET'])
@cache.cached(timeout=10, key_prefix="all_services")
def get_all_services():
    services = db.session.query(Service, ServiceCategory).outerjoin(ServiceCategory, Service.category_id == ServiceCategory.id).all()
    
    service_list = [
        {
            "id": service.id,
            "name": service.name,
            "base_price": service.base_price,
            "time_required": service.time_required,
            "description": service.description,
            "category": category.name if category else None  # Avoids AttributeError
        }
        for service, category in services  # Unpacking the joined query results
    ]
    
    return jsonify({"success": True, "services": service_list, "total": len(service_list)}), 200

# ------------------------------
# ✅ Get a Single Service by ID
# ------------------------------
@services.route('/services/<int:id>', methods=['GET'])
def get_service(id):
    service = db.session.query(Service, ServiceCategory).outerjoin(ServiceCategory, Service.category_id == ServiceCategory.id).filter(Service.id == id).first()
    
    if not service:
        return jsonify({"success": False, "error": "Service not found"}), 404

    service_data, category = service  # Unpacking query result

    return jsonify({
        "success": True,
        "service": {
            "id": service_data.id,
            "name": service_data.name,
            "base_price": service_data.base_price,
            "time_required": service_data.time_required,
            "description": service_data.description,
            "category": category.name if category else None
        }
    }), 200


# ------------------------------
# ✅ Add a New Service (Admin Only)
# ------------------------------
@services.route('/services', methods=['POST'])
@jwt_required()
def add_service():
    data = request.json
    user = get_jwt()

    # Check if user is an admin (assuming role exists in JWT)
    if user.get("role") != 2:
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    required_fields = ["name", "base_price", "time_required", "category_id"]
    if not all(field in data for field in required_fields):
        return jsonify({"success": False, "error": "Missing required fields"}), 400

    category = ServiceCategory.query.get(data["category_id"])
    if not category:
        return jsonify({"success": False, "error": "Invalid category"}), 400

    new_service = Service(
        name=data["name"],
        base_price=data["base_price"],
        time_required=data["time_required"],
        description=data.get("description", "NA"),
        category_id=category.id
    )
    
    db.session.add(new_service)
    db.session.commit()
    
    cache.delete("all_services")

    return jsonify({"success": True, "message": "Service added successfully", "id": new_service.id}), 201

# ------------------------------
# ✅ Edit an Existing Service (Admin Only)
# ------------------------------
@services.route('/services/<int:id>', methods=['PUT'])
@jwt_required()
def edit_service(id):
    service = Service.query.get(id)
    if not service:
        return jsonify({"success": False, "error": "Service not found"}), 404

    user = get_jwt_identity()
    if user.get("role") != 2:
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    data = request.json
    category = ServiceCategory.query.get(data.get("category_id")) if data.get("category_id") else None

    service.name = data.get("name", service.name)
    service.base_price = data.get("base_price", service.base_price)
    service.time_required = data.get("time_required", service.time_required)
    service.description = data.get("description", service.description)
    service.category_id = category.id if category else service.category_id

    db.session.commit()
    
    return jsonify({"success": True, "message": "Service updated successfully"}), 200

# ------------------------------
# ✅ Delete a Service (Admin Only)
# ------------------------------
@services.route('/services/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_service(id):
    service = Service.query.get(id)
    if not service:
        return jsonify({"success": False, "error": "Service not found"}), 404

    user = get_jwt_identity()
    if user.get("role") != 2:
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    if service.service_requests:
        return jsonify({"success": False, "error": "Cannot delete service. It is linked to service requests."}), 400

    db.session.delete(service)
    db.session.commit()
    
    return jsonify({"success": True, "message": "Service deleted successfully"}), 200
