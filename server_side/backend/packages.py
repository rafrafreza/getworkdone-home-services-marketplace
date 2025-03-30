from flask import Blueprint, jsonify, request
from backend.models import db, ServicePackage, ServiceCategory, ServiceProfessional, ProfessionalPackageRequest

packages = Blueprint('packages', __name__)

# ------------------------------
# ✅ Get All Service Packages
# ------------------------------
@packages.route('/packages', methods=['GET'])
def get_all_packages():
    packages = ServicePackage.query.all()
    package_list = [
        {
            "id": package.id,
            "name": package.name,
            "base_price": package.base_price,
            "time_required": package.time_required,
            "description": package.description,
            "category_id": package.category_id,
            "package_type": package.package_type,
            "picture": package.picture,
            "created_at": package.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for package in packages
    ]
    return jsonify({"packages": package_list, "total": len(package_list)}), 200


# ------------------------------
# ✅ Add a New Service Package
# ------------------------------
@packages.route('/packages', methods=['POST'])
def add_package():
    data = request.json

    required_fields = ["name", "base_price", "time_required", "category_id", "package_type"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Validate category_id exists
    category = ServiceCategory.query.get(data["category_id"])
    if not category:
        return jsonify({"error": "Invalid category_id"}), 400

    # Validate package_type
    if data["package_type"] not in [ServicePackage.BASIC, ServicePackage.PREMIUM, ServicePackage.DEEP]:
        return jsonify({"error": "Invalid package_type"}), 400

    new_package = ServicePackage(
        name=data["name"],
        base_price=data["base_price"],
        time_required=data["time_required"],
        description=data.get("description", ""),
        category_id=data["category_id"],
        package_type=data["package_type"],
        picture=data.get("picture")  # ✅ Added picture field
    )
    
    db.session.add(new_package)
    db.session.commit()
    
    return jsonify({"message": "Service package added successfully", "id": new_package.id}), 201


# ------------------------------
# ✅ Edit an Existing Service Package
# ------------------------------
@packages.route('/packages/<int:id>', methods=['PUT'])
def edit_package(id):
    package = ServicePackage.query.get(id)
    if not package:
        return jsonify({"error": "Service package not found"}), 404

    data = request.json
    if "category_id" in data:
        category = ServiceCategory.query.get(data["category_id"])
        if not category:
            return jsonify({"error": "Invalid category_id"}), 400

    if "package_type" in data and data["package_type"] not in [ServicePackage.BASIC, ServicePackage.PREMIUM, ServicePackage.DEEP]:
        return jsonify({"error": "Invalid package_type"}), 400

    package.name = data.get("name", package.name)
    package.base_price = data.get("base_price", package.base_price)
    package.time_required = data.get("time_required", package.time_required)
    package.description = data.get("description", package.description)
    package.category_id = data.get("category_id", package.category_id)
    package.package_type = data.get("package_type", package.package_type)
    package.picture = data.get("picture", package.picture)  # ✅ Added picture field

    db.session.commit()
    
    return jsonify({"message": "Service package updated successfully"}), 200



# ------------------------------
# ✅ Delete a Service Package
# ------------------------------
@packages.route('/packages/<int:id>', methods=['DELETE'])
def delete_package(id):
    package = ServicePackage.query.get(id)
    if not package:
        return jsonify({"error": "Service package not found"}), 404

    db.session.delete(package)
    db.session.commit()
    
    return jsonify({"message": "Service package deleted successfully"}), 200




@packages.route('/assign-professional', methods=['POST'])
def assign_professional_to_package():
    data = request.json
    professional_id = data.get("professional_id")
    package_id = data.get("package_id")

    professional = ServiceProfessional.query.get(professional_id)
    package = ServicePackage.query.get(package_id)

    if not professional:
        return jsonify({"error": "Professional not found"}), 404
    if not package:
        return jsonify({"error": "Service package not found"}), 404

    existing_request = ProfessionalPackageRequest.query.filter_by(professional_id=professional_id, package_id=package_id).first()
    if existing_request:
        return jsonify({"message": "Professional is already assigned", "request_id": existing_request.id}), 200

    new_request = ProfessionalPackageRequest(professional_id=professional.id, package_id=package.id, status='pending')
    db.session.add(new_request)
    db.session.commit()

    return jsonify({"message": "Professional assigned to package successfully", "request_id": new_request.id}), 201
