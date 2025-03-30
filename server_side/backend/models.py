from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ------------------------------
# ✅ Users (Base Model for All Roles)
# ------------------------------
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    fname = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer, default=0)  # 0 = Customer, 1 = Professional, 2 = Admin
    profile_picture = db.Column(db.String(255), default='default_pfp.png', nullable=True)  # Profile Picture URL
    
    # One-to-One Relationships
    admin = db.relationship('Admin', backref='user', uselist=False, cascade="all, delete")
    service_professional = db.relationship('ServiceProfessional', backref='user', uselist=False, cascade="all, delete")
    customer = db.relationship('Customer', backref='user', uselist=False, cascade="all, delete")

# ------------------------------
# ✅ Admin Model (Linked with Users)
# ------------------------------
class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)

# ------------------------------
# ✅ Service Category Model (For Categories like Plumbing, Electricals, etc.)
# ------------------------------
class ServiceCategory(db.Model):
    __tablename__ = 'service_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # Plumbing, Cleaning, etc.
    picture = db.Column(db.String(255), nullable=True)  # URL or file path for category image
    
    # Relationships
    service_packages = db.relationship('ServicePackage', backref='category', lazy=True)


# ------------------------------
# ✅ Service Package Model (Admin-defined Service Packages)
# ------------------------------
class ServicePackage(db.Model):
    __tablename__ = 'service_packages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    base_price = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String(255), nullable=True)  # URL or file path for category image
    time_required = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    BASIC = "Basic"
    PREMIUM = "Premium"
    DEEP = "Deep"
    package_type = db.Column(db.Integer, nullable=False)  # Basic, Premium, Deep
    
    # Relationships
    professional_requests = db.relationship('ProfessionalPackageRequest', back_populates='service_package', lazy=True)  # Use back_populates here
    service_requests = db.relationship('ServiceRequest', back_populates='package', overlaps="professional_requests")



# ------------------------------
# ✅ Professional Package Request Model (Professionals applying to join service package)
# ------------------------------
class ProfessionalPackageRequest(db.Model):
    __tablename__ = 'professional_package_requests'
    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professionals.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('service_packages.id', ondelete="CASCADE"), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending/approved/rejected
    # Relationships
    professional = db.relationship('ServiceProfessional', backref='package_requests')
    service_package = db.relationship('ServicePackage', back_populates="professional_requests") # Use back_populates here


# ------------------------------
# ✅ Service Professional Model
# ------------------------------
class ServiceProfessional(db.Model):
    __tablename__ = 'service_professionals'
    id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    service_type = db.Column(db.String(100), nullable=False)  # Type of service they offer
    experience = db.Column(db.String(150), nullable=False)
    profile_verified = db.Column(db.Boolean, default=False)  # Admin Verified Profile
    blocked = db.Column(db.Boolean, default=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    address = db.Column(db.String(255), nullable=True)
    pin_code = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    base_price_per_hour = db.Column(db.Float, nullable=False)  # Base price per hour
    availability_slots = db.Column(db.String(500), nullable=True)  # JSON field for available time slots
    resume = db.Column(db.Text)  # Store Base64 PDF
    
    # Relationships
    # category = db.relationship('ServiceCategory', backref='professionals')
    service_requests = db.relationship('ServiceRequest', back_populates='professional')
    bookings = db.relationship('Booking', back_populates='professional')

# ------------------------------
# ✅ Customer Model
# ------------------------------
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    address = db.Column(db.String(255), nullable=True)
    pin_code = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    blocked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    service_requests = db.relationship('ServiceRequest', back_populates='customer')
    bookings = db.relationship('Booking', back_populates='customer')

# ------------------------------
# ✅ Service Model (Created by Admin)
# ------------------------------
class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'), nullable=False)


    # Relationships
    service_requests = db.relationship('ServiceRequest', back_populates='service')

# ------------------------------
# ✅ Service Request Model (Customer Requests a Service)
# ------------------------------
class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)    # For general service requests
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete="CASCADE"), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professionals.id'), nullable=True)
    package_id = db.Column(db.Integer, db.ForeignKey('service_packages.id'), nullable=True)  # For package-based service requests
    
    service_dateTime = db.Column(db.DateTime, nullable=False)  # When customer wants the service
    date_of_request = db.Column(db.DateTime, default=datetime.utcnow)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    
    service_status = db.Column(db.String(50), default='requested')  # requested/assigned/closed/cancelled
    payment_status = db.Column(db.String(50), default='pending')  # pending/successful/failed
    ratings = db.Column(db.Integer, nullable=True)
    reviews = db.Column(db.Text, nullable=True)
    
    # Relationships
    service = db.relationship('Service', back_populates='service_requests')
    customer = db.relationship('Customer', back_populates='service_requests')
    professional = db.relationship('ServiceProfessional', back_populates='service_requests')
    package = db.relationship('ServicePackage', back_populates='service_requests')

# ------------------------------
# ✅ Booking Model (For Scheduled Services)
# ------------------------------
class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)

    # Add ON DELETE CASCADE to customer_id and professional_id
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professionals.id', ondelete='CASCADE'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)

    category = db.Column(db.String(50), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)  # Scheduled Date
    time_slot = db.Column(db.String(50), nullable=False)  # Morning/Afternoon/Evening
    price = db.Column(db.Float, nullable=False)  # Final Price Based on Hours
    
    status = db.Column(db.String(50), default='pending')  # pending/confirmed/completed/cancelled
    reviews = db.Column(db.Text, nullable=True)
    ratings = db.Column(db.Integer, nullable=True)
    payment_status = db.Column(db.String(50), default='pending')  # pending/successful/failed
    payment_method = db.Column(db.String(50), nullable=True)  # Card, UPI, PayPal, etc.

    # Relationships
    customer = db.relationship('Customer', back_populates='bookings', passive_deletes=True)
    professional = db.relationship('ServiceProfessional', back_populates='bookings', passive_deletes=True)
    service = db.relationship('Service')




# ------------------------------
# ✅ Notification Model
# ------------------------------
class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)  # Mark as read/unread
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('Users', backref='notifications')

