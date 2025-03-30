from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from backend.models import *

dashboard = Blueprint('dashboard', __name__)

# ------------------------------
# ✅ Dashboard for Customers
# ------------------------------
@dashboard.route('/customer', methods=['GET'])
@jwt_required()
def customer_dashboard():
    current_user_id = get_jwt_identity()
    claims = get_jwt()

    # Ensure the user is a Customer
    if claims.get("role") != 0:
        return jsonify({"message": "Unauthorized access. Customers only."}), 403

    # Fetch user and customer details
    user = Users.query.filter_by(id=current_user_id).first()
    customer = Customer.query.filter_by(id=current_user_id).first()
    
    if not customer or not user:
        return jsonify({"message": "Customer not found"}), 404

    return jsonify({
        "message": "Welcome to your dashboard, Customer!",
        "customer_info": {
            "id": customer.id,
            "name": user.fname,
            "phone": user.phone,  # Fetching phone from Users model
            "profile_picture": user.profile_picture,  # Fetching pfp from Users model
            "address": customer.address if customer.address else "Update your Address",
            "pin_code": customer.pin_code,
            "city": customer.city,
            "created_at": customer.created_at
        }
    }), 200



@dashboard.route('/customer/update', methods=['PUT'])
@jwt_required()
def update_custo_profile():
    try:
        user_id = get_jwt_identity()  # Get the authenticated user ID
        data = request.json  # Get JSON data from request
        
        # Fetch user from the database
        customer = Customer.query.get(user_id)
        user = Users.query.get(user_id)
        if not customer:
            return jsonify({"message": "User not found"}), 404
        
        # Update allowed fields only
        if "phone" in data:
            user.phone = data["phone"]
        if "name" in data:
            user.fname = data["name"]
        if "city" in data:
            customer.city = data["city"]
        if "pin_code" in data:
            customer.pin_code = data["pin_code"]
        if "address" in data:
            customer.address = data["address"]

        # Commit changes to the database
        db.session.commit()
        
        return jsonify({"message": "Profile updated successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating profile", "error": str(e)}), 500


# ------------------------------
# ✅ Dashboard for Service Professionals
# ------------------------------
@dashboard.route('/professional', methods=['GET'])
@jwt_required()
def professional_dashboard():
    current_user_id = get_jwt_identity()
    claims = get_jwt()

    # Ensure the user is a Service Professional
    if claims.get("role") != 1:
        return jsonify({"message": "Unauthorized access. Service Professionals only."}), 403

    # Fetch user and professional details
    user = Users.query.filter_by(id=current_user_id).first()
    professional = ServiceProfessional.query.filter_by(id=current_user_id).first()
    
    if not professional or not user:
        return jsonify({"message": "Service Professional not found"}), 404

    return jsonify({
        "message": "Welcome to your dashboard, Service Professional!",
        "professional_info": {
            "id": professional.id,
            "name": user.fname,
            "email": professional.email, 
            "phone": user.phone,  # Fetching phone from Users model
            "profile_picture": user.profile_picture,
            "experience": professional.experience,
            "service_type": professional.service_type,
            "address": professional.address,
            "pin_code": professional.pin_code,
            "city": professional.city,
            "base_price": professional.base_price_per_hour,
            "availability": professional.availability_slots,
            "profile_verified": professional.profile_verified,
            "blocked": professional.blocked,
            "created_at": professional.created_at
        }
    }), 200


@dashboard.route('/professional/update', methods=['PUT'])
@jwt_required()
def update_profes_profile():
    try:
        user_id = get_jwt_identity()  # Get the authenticated user ID
        data = request.json  # Get JSON data from request
        
        # Fetch user from the database
        professional = ServiceProfessional.query.get(user_id)
        user = Users.query.get(user_id)
        if not professional:
            return jsonify({"message": "User not found"}), 404
        
        # Update allowed fields only
        if "name" in data:
            user.fname = data["name"]
        if "service_type" in data:
            professional.service_type = data["service_type"]
        if "experience" in data:
            professional.experience = data["experience"]
        if "city" in data:
            professional.city = data["city"]
        if "pin_code" in data:
            professional.pin_code = data["pin_code"]
        if "base_price" in data:
            professional.base_price_per_hour = data["base_price"]

        # Commit changes to the database
        db.session.commit()
        
        return jsonify({"message": "Profile updated successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating profile", "error": str(e)}), 500



# ------------------------------
# ✅ Dashboard for Admins
# ------------------------------
@dashboard.route('/admin', methods=['GET'])
@jwt_required()
def admin_dashboard():
    current_user_id = get_jwt_identity()
    claims = get_jwt()

    # Ensure the user is an Admin
    if claims.get("role") != 2:
        return jsonify({"message": "Unauthorized access. Admins only."}), 403

    # Fetch user and admin details
    user = Users.query.filter_by(id=current_user_id).first()
    admin = Admin.query.filter_by(id=current_user_id).first()

    if not admin or not user:
        return jsonify({"message": "Admin not found"}), 404

    return jsonify({
        "message": "Welcome to your dashboard, Admin!",
        "admin_info": {
            "id": admin.id,
            "phone": user.phone,
            "email": admin.email,
            "fname": user.fname,  # Fetching first name from Users model
            "profile_picture": user.profile_picture
        }
    }), 200
