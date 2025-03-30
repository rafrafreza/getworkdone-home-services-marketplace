from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
# from backend.models import Users, ServiceProfessional, Customer, Admin

home = Blueprint('home',__name__)

@home.route("/", methods=["GET"])
def landing():
    print("App landing page...")