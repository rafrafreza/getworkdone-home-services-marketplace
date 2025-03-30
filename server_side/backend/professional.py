from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import *

professional = Blueprint('professional', __name__)

# ✅ View Available Packages (Exclude Already Applied or Joined Packages)
@professional.route('/professionals/packages/available', methods=['GET'])
@jwt_required()
def available_packages():
    """Get all packages that the professional has NOT applied for"""
    professional_id = get_jwt_identity()

    # Get all package IDs that the professional has applied for
    applied_packages = db.session.query(ProfessionalPackageRequest.package_id).filter_by(professional_id=professional_id).all()
    applied_package_ids = {pkg[0] for pkg in applied_packages}  # Convert to a set

    # Get all available packages (excluding applied ones)
    available_packages = ServicePackage.query.filter(~ServicePackage.id.in_(applied_package_ids)).all()

    return jsonify([
        {
            "id": pkg.id,
            "name": pkg.name,
            "description": pkg.description,
            "base_price": pkg.base_price,
            "time_required": pkg.time_required,
            "category_id": pkg.category_id,
            "created_at": pkg.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        } for pkg in available_packages
    ])


# ✅ Apply for a service package
@professional.route('/professionals/packages/apply', methods=['POST'])
@jwt_required()
def apply_package():
    """Professional applies for a package"""
    professional_id = get_jwt_identity()
    data = request.json
    package_id = data.get('package_id')

    if not package_id:
        return jsonify({"error": "Package ID is required"}), 400

    # Check if package exists
    package = ServicePackage.query.get(package_id)
    if not package:
        return jsonify({"error": "Package not found"}), 404

    # Check if the professional already applied
    existing_request = ProfessionalPackageRequest.query.filter_by(professional_id=professional_id, package_id=package_id).first()
    if existing_request:
        return jsonify({"error": "You have already applied for this package"}), 400

    # Create a new request
    new_request = ProfessionalPackageRequest(professional_id=professional_id, package_id=package_id, status="pending")
    db.session.add(new_request)
    db.session.commit()

    return jsonify({"message": "Package request submitted successfully"}), 201


# ✅ Get all package requests of a professional
@professional.route('/professionals/packages/my-requests', methods=['GET'])
@jwt_required()
def my_package_requests():
    """Get all packages a professional has applied for"""
    professional_id = get_jwt_identity()

    requests = ProfessionalPackageRequest.query.filter_by(professional_id=professional_id).all()

    return jsonify([
        {
            "id": req.id,
            "package_id": req.package_id,
            "package_name": req.service_package.name,
            "status": req.status
        } for req in requests
    ])


# ✅ Get all joined packages (Only Approved Requests)
@professional.route('/professionals/packages/joined', methods=['GET'])
@jwt_required()
def joined_packages():
    """Get all packages that the professional has been approved for (joined)"""
    professional_id = get_jwt_identity()

    # Get all approved package requests
    joined_requests = ProfessionalPackageRequest.query.filter_by(professional_id=professional_id, status="approved").all()

    return jsonify([
        {
            "id": req.package_id,
            "name": req.service_package.name,
            "description": req.service_package.description,
            "base_price": req.service_package.base_price,
            "time_required": req.service_package.time_required,
            "category_id": req.service_package.category_id,
            "created_at": req.service_package.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        } for req in joined_requests
    ])

@professional.route('/professional/service-requests', methods=['GET'])
def get_service_requests():
    # Filter requests that are 'requested' and have a valid service_id
    service_requests = ServiceRequest.query.filter(
        ServiceRequest.service_status == 'requested',
        ServiceRequest.service_id.isnot(None)  # Ensure service_id is not null
    ).all()
    
    return jsonify([{
        'id': req.id,
        'service': {'name': req.service.name,
                    'service_price': req.service.base_price,
                    'service_dateTime': req.service_dateTime,},  # Use relationship to get service name
        'customer': {'fname': req.customer.user.fname}  # Use relationship to get customer fname
    } for req in service_requests])

@professional.route('/professional/package-requests', methods=['GET'])
@jwt_required()
def get_package_requests():
    professional_id = get_jwt_identity()

    if not professional_id:
        return jsonify({"error": "Professional ID is required"}), 400

    # Get approved packages that the professional has joined
    approved_packages = db.session.query(ProfessionalPackageRequest.package_id).filter(
        ProfessionalPackageRequest.professional_id == professional_id,
        ProfessionalPackageRequest.status == 'approved'
    ).subquery()

    # Fetch package requests only for those packages
    package_requests = ServiceRequest.query.filter(
        ServiceRequest.service_status == 'requested',
        ServiceRequest.package_id.in_(approved_packages)
    ).all()

    return jsonify([{
        'id': req.id,
        'package': {
            'name': req.package.name,
            'package_price': req.package.base_price,
            "description": req.package.description,
            'service_dateTime': req.service_dateTime
        },
        # 'customer': {
        #     'fname': req.customer.fname  # Assuming 'customer' relationship exists
        # }
    } for req in package_requests])


@professional.route('/professional/direct-bookings', methods=['GET'])
@jwt_required()
def get_direct_bookings():
    professional_id = get_jwt_identity()
    print("Professional ID from JWT:", professional_id)  # Debugging

    direct_bookings = Booking.query.filter_by(
        professional_id=professional_id, status='pending' 
    ).all()

    print("Direct Bookings Found:", direct_bookings)  # Debugging

    return jsonify([{
        'id': booking.id,
        'service': {'date': booking.booking_date,
                    'time_slot': booking.time_slot,
                    'price': booking.price,},
        'customer': {'fname': booking.customer.user.fname}
    } for booking in direct_bookings])



@professional.route('professional/accept-service/<int:id>', methods=['POST'])
@jwt_required()
def accept_service(id):
    professional_id = get_jwt_identity()
    service_request = ServiceRequest.query.get(id)
    if not service_request:
        return jsonify({'error': f'Service request {id} not found'}), 404

    print(f"ServiceRequest: {service_request.id}, service_id: {service_request.service_id}")

    if service_request.service_id is None:
        return jsonify({'error': f'Service request {id} is not linked to a service'}), 400

    service_request.service_status = 'assigned'
    service_request.professional_id = professional_id
    db.session.commit()

    return jsonify({'message': 'Service request accepted successfully'})


@professional.route('professional/accept-package/<int:id>', methods=['POST'])
@jwt_required()
def accept_package(id):
    professional_id = get_jwt_identity()
    package_request = ServiceRequest.query.get(id)
    if not package_request or package_request.package_id is None:
        return jsonify({'error': 'Package request not found or invalid'}), 404

    package_request.service_status = 'assigned'  # Update status to assigned
    package_request.professional_id = professional_id
    db.session.commit()

    return jsonify({'message': 'Package request accepted successfully'})


@professional.route('professional/accept-booking/<int:id>', methods=['POST'])
def accept_booking(id):
    booking_request = Booking.query.get(id)
    if not booking_request:
        return jsonify({'error': 'Booking request not found'}), 404

    booking_request.status = 'accepted'  
    db.session.commit()

    return jsonify({'message': 'Booking accepted successfully'})


@professional.route('professional/reject-booking/<int:id>', methods=['POST'])
def reject_booking(id):
    booking_request = Booking.query.get(id)
    if not booking_request:
        return jsonify({'error': 'Booking request not found'}), 404

    booking_request.status = 'rejected'  # Mark as closed/rejected
    db.session.commit()

    return jsonify({'message': 'Booking rejected successfully'})


# ✅ 1. Get all accepted service requests for a professional
@professional.route('professionals/accepted-services', methods=['GET'])
@jwt_required()
def get_accepted_services():
    professional_id = get_jwt_identity()

    accepted_services = ServiceRequest.query.filter(
        ServiceRequest.professional_id == professional_id,
        ServiceRequest.package_id == None, 
        ServiceRequest.service_status == "assigned"
    ).all()

    services_data = [
        {
            "id": sr.id,
            "service_name": sr.service.name if sr.service else "N/A",
            "customer_id": sr.customer_id,
            "price": sr.service.base_price,
            "status": sr.service_status,
            "date_of_request": sr.date_of_request,
            "Scheduled_Date": sr.service_dateTime
        }
        for sr in accepted_services
    ]
    print(services_data)
    return jsonify(services_data), 200


# ✅ 2. Get all accepted packages for a professional
@professional.route('professionals/accepted-packages', methods=['GET'])
@jwt_required()
def get_accepted_packages():
    professional_id = get_jwt_identity()

    accepted_packages = ServiceRequest.query.filter(
        ServiceRequest.professional_id == professional_id,
        ServiceRequest.service_id == None,
        ServiceRequest.service_status == "assigned"
    ).all()

    packages_data = [
        {
            "id": sr.id,
            "package_name": sr.package.name if sr.package else "N/A",
            "customer_id": sr.customer_id,
            "description": sr.package.description,
            "price": sr.package.base_price,
            "status": sr.service_status,
            "date_of_request": sr.date_of_request,
            "Scheduled_Date": sr.service_dateTime
        }
        for sr in accepted_packages
    ]
    print(packages_data)
    return jsonify(packages_data), 200


# ✅ 3. Get all confirmed bookings for a professional
@professional.route('professionals/accepted-bookings', methods=['GET'])
@jwt_required()
def get_accepted_bookings():
    professional_id = get_jwt_identity()

    confirmed_bookings = Booking.query.filter_by(
        professional_id=professional_id, status="accepted"
    ).all()

    bookings_data = [
        {
            "id": booking.id,
            "service_name": booking.service.service_type if booking.service else "N/A",
            "customer_id": booking.customer_id,
            "Scheduled_Date": booking.booking_date,
            "time_slot": booking.time_slot,
            "price": booking.price,
            "status": booking.status
        }
        for booking in confirmed_bookings
    ]
    return jsonify(bookings_data), 200


# ✅ 1. Get all completed service requests for a professional
@professional.route('professionals/completed-services', methods=['GET'])
@jwt_required()
def get_completed_services():
    professional_id = get_jwt_identity()

    completed_services = ServiceRequest.query.filter(
        ServiceRequest.professional_id == professional_id,
        ServiceRequest.package_id == None, 
        ServiceRequest.service_status == "completed"
    ).all()

    services_data = [
        {
            "id": sr.id,
            "service_name": sr.service.name if sr.service else "N/A",
            "customer_id": sr.customer_id,
            "price": sr.service.base_price,
            "status": sr.service_status,
            "date_of_request": sr.date_of_request,
            "Scheduled_Date": sr.service_dateTime,
            "payment_status": sr.payment_status if sr.payment_status else "Not Available",
            "ratings": sr.ratings if sr.ratings is not None else "Not Rated",
            "reviews": sr.reviews if sr.reviews else "No Review"
        }
        for sr in completed_services
    ]
    print(services_data)
    return jsonify(services_data), 200


# ✅ 2. Get all completed packages for a professional
@professional.route('professionals/completed-packages', methods=['GET'])
@jwt_required()
def get_completed_packages():
    professional_id = get_jwt_identity()

    completed_packages = ServiceRequest.query.filter(
        ServiceRequest.professional_id == professional_id,
        ServiceRequest.service_id == None,
        ServiceRequest.service_status == "completed"
    ).all()

    packages_data = [
        {
            "id": sr.id,
            "package_name": sr.package.name if sr.package else "N/A",
            "customer_id": sr.customer_id,
            "description": sr.package.description,
            "price": sr.package.base_price,
            "status": sr.service_status,
            "date_of_request": sr.date_of_request,
            "Scheduled_Date": sr.service_dateTime,
            "payment_status": sr.payment_status if sr.payment_status else "Not Available",
            "ratings": sr.ratings if sr.ratings is not None else "Not Rated",
            "reviews": sr.reviews if sr.reviews else "No Review"
        }
        for sr in completed_packages
    ]
    print(packages_data)
    return jsonify(packages_data), 200


# ✅ 3. Get all completed bookings for a professional
@professional.route('professionals/completed-bookings', methods=['GET'])
@jwt_required()
def get_completed_bookings():
    professional_id = get_jwt_identity()

    completed_bookings = Booking.query.filter_by(
        professional_id=professional_id, status="completed"
    ).all()

    bookings_data = [
        {
            "id": booking.id,
            "service_name": booking.service.service_type if booking.service else "N/A",
            "customer_id": booking.customer_id,
            "Scheduled_Date": booking.booking_date,
            "time_slot": booking.time_slot,
            "price": booking.price,
            "status": booking.status,
            "payment_status": booking.payment_status if booking.payment_status else "Not Available",
            "payment_method": booking.payment_method if booking.payment_method else "Not Provided",
            "ratings": booking.ratings if booking.ratings is not None else "Not Rated",
            "reviews": booking.reviews if booking.reviews else "No Review"
        }
        for booking in completed_bookings
    ]
    return jsonify(bookings_data), 200
