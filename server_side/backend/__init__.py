from flask import Flask
from backend.models import *
from backend.mail import mail  # Import mail instance
from backend.api import register_apis  # Import the function from api.py
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from flask_cors import CORS  # Add this import
from backend.cache import cache

def create_app():
    GetWorkDone = Flask(__name__)
    GetWorkDone.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev-secret-key")
    GetWorkDone.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///GetWorkDone.db'
    GetWorkDone.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    GetWorkDone.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret-key")
    GetWorkDone.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)  # Token expiration time
    GetWorkDone.config["UPLOAD_FOLDER"] =  os.path.join(os.getcwd(), "static/uploads")
    # Enable CORS for all routes
    CORS(GetWorkDone, resources={r"/*": {"origins": ["http://localhost:5173"]}})
    
    # Mail Configuration
    GetWorkDone.config["MAIL_SERVER"] = "smtp.gmail.com"
    GetWorkDone.config["MAIL_PORT"] = 587
    GetWorkDone.config["MAIL_USE_TLS"] = True
    GetWorkDone.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
    GetWorkDone.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
    GetWorkDone.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER", os.environ.get("MAIL_USERNAME"))
    
    mail.init_app(GetWorkDone)  # Initialize Flask-Mail with app

    # Initialize extensions
    db.init_app(GetWorkDone)
    jwt = JWTManager(GetWorkDone)  # Initialize JWTManager
    
    # Register APIs (blueprints)
    register_apis(GetWorkDone)

    # Redis cache configuration
    GetWorkDone.config['CACHE_TYPE'] = 'RedisCache'
    GetWorkDone.config['CACHE_REDIS_HOST'] = 'localhost'
    GetWorkDone.config['CACHE_REDIS_PORT'] = 6379
    GetWorkDone.config['CACHE_REDIS_DB'] = 0
    GetWorkDone.config['CACHE_DEFAULT_TIMEOUT'] = 10  

    cache.init_app(GetWorkDone)

    print("App started successfully.....✨😍")

    # ------------------ Db Implementation and Admin Registration ------------------------------
    with GetWorkDone.app_context():
        db.create_all()

        try:
            # Check if the admin user already exists based on the phone number
            if db.session.query(Users).filter_by(phone='9876543210').first() is None:
                # Creating an admin user
                admin_user = Users(
                    phone='9876543210',
                    password=generate_password_hash('12345'),  
                    fname='Administration',
                    role=2,  # Admin role
                    profile_picture = 'deafault_pfp.jpg'
                )
                db.session.add(admin_user)
                db.session.flush()  # Flush but don't commit

                try:
                    # Creating an admin profile
                    admin = Admin(
                        id=admin_user.id,
                        email='admin@gmail.com')
                    db.session.add(admin)
                    db.session.commit()  # Commit only if everything is successful
                except Exception as e:
                    db.session.rollback()  # Rollback if there's any issue
                    print(f"Error creating admin profile: {e}")

            else:
                print("Admin user already exists with this phone number.")

            # # Check if the service professional user already exists based on the phone number
            # if db.session.query(Users).filter_by(phone='1231231231').first() is None:
            #     # Creating a test service professional
            #     professional_user = Users(
            #         phone='1231231231',
            #         password=generate_password_hash('12345'),
            #         fname='Test Professional',
            #         role=1,  # Service Professional role
            #         profile_picture = 'deafault_pfp.jpg'
            #     )
            #     db.session.add(professional_user)
            #     db.session.flush()  # Flush but don't commit

            #     try:
            #         # Creating a service professional profile
            #         professional = ServiceProfessional(
            #             id=professional_user.id,
            #             email='professional1@gmail.com',
            #             service_type='Cleaning',
            #             experience='2 years',
            #             address='Gali no 22, Okhla, New Delhi',
            #             pin_code='112233',
            #             city='New Delhi',
            #             base_price_per_hour=20.0,  # Example price per hour
            #             availability_slots='{"Monday": ["9 AM - 12 PM", "2 PM - 5 PM"]}'  # JSON format availability
            #         )
            #         db.session.add(professional)
            #         db.session.commit()  # Commit only if everything is successful
            #     except Exception as e:
            #         db.session.rollback()  # Rollback if there's any issue
            #         print(f"Error creating service professional profile: {e}")

            # else:
            #     print("Service Professional user already exists with this phone number.")

            # # Check if the customer user already exists based on the phone number
            # if db.session.query(Users).filter_by(phone='5675675675').first() is None:
            #     # Creating a test customer
            #     customer_user = Users(
            #         phone='5675675675',
            #         password=generate_password_hash('12345'),
            #         fname='Test Customer',
            #         role=0,  # Customer role
            #         profile_picture = 'deafault_pfp.jpg'
            #     )
            #     db.session.add(customer_user)
            #     db.session.flush()  # Flush but don't commit

            #     try:
            #         # Creating a customer profile
            #         customer = Customer(
            #             id=customer_user.id,
            #             address='Okhla, Delhi',
            #             pin_code='110023',
            #             city='Delhi'
            #         )
            #         db.session.add(customer)
            #         db.session.commit()  # Commit only if everything is successful
            #     except Exception as e:
            #         db.session.rollback()  # Rollback if there's any issue
            #         print(f"Error creating customer profile: {e}")

            # else:
            #     print("Customer user already exists with this phone number.")

        except Exception as e:
            db.session.rollback()  # Rollback any transaction in case of failure
            print(f"Unexpected error: {e}")

    return GetWorkDone
