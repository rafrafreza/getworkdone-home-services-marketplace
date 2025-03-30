from flask import Blueprint, request, jsonify, current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from backend.models import *
import os
from werkzeug.utils import secure_filename
# import datetime

auth = Blueprint('auth', __name__)



# Store invalidated JWTs
jwt_blocklist = set()


# Customer Signup Route
@auth.route('/signup/customer', methods=['POST'])
def signup_customer():
    data = request.form

    # Print received data for debugging
    # print("Received JSON data:", data)

    if not data:
        return jsonify({"message": "No data received"}), 400

    phone = data.get('phone')
    password = data.get('password')
    fname = data.get('fname')
    city = data.get('city')
    pin_code = data.get('pin_code')
    profile_picture = data.get('profile_picture')

    if not phone or not password or not fname or not city or not pin_code:
        return jsonify({"message": "Missing required fields"}), 400

    # Check if user exists
    if Users.query.filter_by(phone=phone).first():
        return jsonify({"message": "Phone number already registered"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Create new user
    new_user = Users(phone=phone, password=hashed_password, fname=fname, role=0, profile_picture=profile_picture)
    db.session.add(new_user)
    db.session.flush()

    # Create customer entry
    new_customer = Customer(id=new_user.id, city=city, pin_code=pin_code)
    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"message": "Customer created successfully"}), 201



@auth.route('/signup/professional', methods=['POST'])
def signup_professional():
    data = request.get_json()

    phone = data.get('phone')
    password = data.get('password')
    fname = data.get('fname')
    email = data.get('email')
    service_type = data.get('service_type')
    experience = data.get('experience')
    city = data.get('city')
    pin_code = data.get('pin_code')
    base_price_per_hour = data.get('base_price_per_hour')
    profile_picture = data.get('profile_picture')
    resume_base64 = data.get('resume')

    # Check for missing required fields
    missing_fields = [field for field in ['phone', 'password', 'fname', 'email', 'service_type', 'experience'] if not data.get(field)]
    if missing_fields:
        return jsonify({"message": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    # Check if user already exists
    if Users.query.filter_by(phone=phone).first():
        return jsonify({"message": "Phone number already registered"}), 400

    # Hash the password
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Create new user
    new_user = Users(
        phone=phone, 
        password=hashed_password, 
        fname=fname, 
        role=1, 
        profile_picture=profile_picture
    )
    db.session.add(new_user)
    db.session.flush()

    # Create professional entry
    new_professional = ServiceProfessional(
        id=new_user.id, 
        email=email, 
        service_type=service_type, 
        experience=experience, 
        city=city, 
        pin_code=pin_code, 
        base_price_per_hour=base_price_per_hour, 
        resume=resume_base64
    )
    db.session.add(new_professional)
    db.session.commit()

    return jsonify({"message": "Service Professional created successfully"}), 201


# Login Route (Universal for all users)
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('phone') or not data.get('password'):
        return jsonify({"message": "Missing phone or password"}), 400

    phone = data['phone']
    password = data['password']

    # Find user by phone
    user = Users.query.filter_by(phone=phone).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid phone or password"}), 401

    if user.role == 0:
        custo = Customer.query.filter_by(id = user.id).first()
        if custo.blocked == True:
            return jsonify("You have been blocked by Administrator...Contact Us.")
    if user.role == 1:
        prof = ServiceProfessional.query.filter_by(id = user.id).first()
        if prof.profile_verified == 0:
            print("Profile not verified")
            return jsonify("Profile not verified")
        if prof.blocked == True:
            return jsonify("You have been blocked by Administrator...Contact Us.")

    # Generate JWT token
    access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    print("access_token:", access_token, "role:", user.role)
    return jsonify({"access_token": access_token, "role": user.role}), 200


# Logout Route (Universal for all users)
@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # Get the unique token identifier
    jwt_blocklist.add(jti)  # Add token to blocklist
    return jsonify({"message": "Logged out successfully"}), 200



# Protected Route Example (User Info)
@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()  # Returns the user ID as a string
    claims = get_jwt()  # Returns the custom claims
    role = claims.get("role")

    return jsonify({"message": f"Welcome user {current_user} with role {role}!"}), 200


