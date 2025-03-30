from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import *
from datetime import datetime

customer = Blueprint('customer', __name__)



# ✅ Create a new service request
@customer.route("/customers/service-requests/create", methods=["POST"])
@jwt_required()
def create_service_request():
    customer_id = get_jwt_identity()  # Get customer ID from JWT token
    data = request.get_json()
    service_id = data.get("service_id")
    package_id = data.get("package_id")
    service_dateTime_str = data.get('service_dateTime')

    if not (service_id or package_id) or not service_dateTime_str:
        return jsonify({"error": "Missing required fields"}), 400

    service_dateTime_str = service_dateTime_str.replace("T", " ")  # Replace 'T' with a space
    service_dateTime = datetime.strptime(service_dateTime_str, "%Y-%m-%d %H:%M")

    new_request = ServiceRequest(
        service_id=service_id,
        package_id=package_id,
        customer_id=customer_id,  # Use customer_id from JWT
        service_dateTime=service_dateTime
    )

    db.session.add(new_request)
    db.session.commit()

    return jsonify({ 
        "message": "Service request created successfully!",
        "customer_id": customer_id,
        "service_id": service_id,
        "package_id": package_id,
        "service_dateTime": service_dateTime
    }), 201

# # ✅ Get all service requests of a customer
# @customer.route('/customers/service-requests/my-requests', methods=['GET'])
# @jwt_required()
# def my_service_requests():
#     customer_id = get_jwt_identity()
#     # customer_id = request.args.get('customer_id')
#     requests = ServiceRequest.query.filter_by(customer_id=customer_id).all()
#     return jsonify([{'id': r.id, 'service_id': r.service_id, 'status': r.service_status} for r in requests])

# ✅ Cancel a service request
# @customer.route('/customers/service-requests/cancel/<int:id>', methods=['PUT'])
# def cancel_service_request(id):
#     request = ServiceRequest.query.get(id)
#     if not request:
#         return jsonify({'error': 'Request not found'}), 404
#     request.service_status = 'cancelled'
#     db.session.commit()
#     return jsonify({'message': 'Service request cancelled'})

@customer.route('/customers/bookings/create', methods=['POST'])
@jwt_required()
def create_booking():
    data = request.json
    print(f"Received request data: {data}")  # Debug request data

    customer_id = get_jwt_identity()
    if not customer_id:
        print("Error: User not authenticated")
        return jsonify({"error": "User not authenticated"}), 401

    
    try:
        booking_date = datetime.strptime(data["booking_date"], "%Y-%m-%d").date()
    except Exception as e:
        print(f"Error: Invalid booking_date format - {e}")
        return jsonify({"error": "Invalid booking_date format, expected YYYY-MM-DD"}), 400

    try:
        new_booking = Booking(
            customer_id=customer_id,
            professional_id=data.get('professional_id'),
            service_id=data.get('service_id'),
            category = data.get('category'),
            booking_date=booking_date,
            time_slot=data.get('time_slot'),
            price=data.get('price')
        )
        db.session.add(new_booking)
        db.session.commit()
        return jsonify({'message': 'Booking created'})
    except Exception as e:
        print(f"Database Error: {e}")
        db.session.rollback()
        return jsonify({"error": "Failed to create booking"}), 500


#get Customer service requests
# Import necessary models
from sqlalchemy.orm import aliased

@customer.route('/customer/service-requests', methods=['GET'])
@jwt_required()
def get_service_requests():
    customer_id = get_jwt_identity()

    # Alias for professional user
    ProfessionalUser = aliased(Users)

    # Fetch only service requests (package_id is NULL)
    service_requests = db.session.query(
        ServiceRequest.id,
        ServiceRequest.service_id,
        ServiceRequest.professional_id,
        ServiceRequest.service_status,
        ServiceRequest.date_of_request,
        ServiceRequest.service_dateTime,
        ServiceRequest.date_of_completion,
        ServiceRequest.payment_status,
        ServiceRequest.ratings,
        ServiceRequest.reviews,
        Service.name.label('service_name'),
        Service.base_price.label('service_price'),
        ServiceCategory.name.label('category_name'),
        ProfessionalUser.fname.label('professional_name')
    ).join(Service, ServiceRequest.service_id == Service.id) \
     .join(ServiceCategory, Service.category_id == ServiceCategory.id) \
     .outerjoin(ServiceProfessional, ServiceRequest.professional_id == ServiceProfessional.id) \
     .outerjoin(ProfessionalUser, ServiceProfessional.id == ProfessionalUser.id) \
     .filter(ServiceRequest.customer_id == customer_id, ServiceRequest.package_id.is_(None)) \
     .all()

    # Format results
    results = [
        {
            'id': sr.id,
            'service_name': sr.service_name or "N/A",
            'category_name': sr.category_name or "N/A",
            'service_price': sr.service_price or "N/A",
            'service_id': sr.service_id,
            'professional_name': sr.professional_name or "Not Assigned",
            'status': sr.service_status,
            'payment_status': sr.payment_status or "N/A",
            'ratings': sr.ratings if sr.ratings is not None else "Not Rated",
            'reviews': sr.reviews or "Not Reviewed",
            'request_date': sr.date_of_request.strftime('%Y-%m-%d %H:%M:%S'),
            'service_dateTime': sr.service_dateTime.strftime('%Y-%m-%d %H:%M:%S'),
            'completion_date': sr.date_of_completion.strftime('%Y-%m-%d %H:%M:%S') if sr.date_of_completion else None
        } for sr in service_requests
    ]

    return jsonify(results), 200



@customer.route('/customer/package-requests', methods=['GET'])
@jwt_required()
def get_package_requests():
    customer_id = get_jwt_identity()

    # Alias for professional user
    ProfessionalUser = aliased(Users)

    # Fetch only package requests (service_id is NULL)
    package_requests = db.session.query(
        ServiceRequest.id,
        ServiceRequest.package_id,
        ServiceRequest.professional_id,
        ServiceRequest.service_status,
        ServiceRequest.date_of_request,
        ServiceRequest.service_dateTime,
        ServiceRequest.date_of_completion,
        ServiceRequest.payment_status,
        ServiceRequest.ratings,
        ServiceRequest.reviews,
        ServicePackage.name.label('package_name'),
        ServicePackage.base_price.label('package_price'),
        ServiceCategory.name.label('category_name'),
        ProfessionalUser.fname.label('professional_name')
    ).join(Service, ServiceRequest.package_id == Service.id) \
     .join(ServiceCategory, Service.category_id == ServiceCategory.id) \
     .outerjoin(ServiceProfessional, ServiceRequest.professional_id == ServiceProfessional.id) \
     .outerjoin(ProfessionalUser, ServiceProfessional.id == ProfessionalUser.id) \
     .filter(ServiceRequest.customer_id == customer_id, ServiceRequest.service_id.is_(None)) \
     .all()

    # Format results
    results = [
        {
            'id': pr.id,
            'package_name': pr.package_name or "N/A",
            'category_name': pr.category_name or "N/A",
            'package_price': pr.package_price or "N/A",
            'package_id': pr.package_id,
            'professional_name': pr.professional_name or "Not Assigned",
            'status': pr.service_status,
            'payment_status': pr.payment_status or "N/A",
            'ratings': pr.ratings if pr.ratings is not None else "Not Rated",
            'reviews': pr.reviews or "Not Reviewed",
            'request_date': pr.date_of_request.strftime('%Y-%m-%d %H:%M:%S'),
            'service_dateTime': pr.service_dateTime.strftime('%Y-%m-%d %H:%M:%S'),
            'completion_date': pr.date_of_completion.strftime('%Y-%m-%d %H:%M:%S') if pr.date_of_completion else None
        } for pr in package_requests
    ]
    print(results)
    return jsonify(results), 200



# @customer.route('/customer/booking-requests', methods=['GET'])
# @jwt_required()
# def get_booking_requests():
#     customer_id = get_jwt_identity()
#     customer = Customer.query.get(customer_id)

#     if not customer:
#         return jsonify({'error': 'Customer not found'}), 404

#     bookings = customer.bookings  # Relationship from Customer -> Bookings

#     results = [
#         {
#             'id': b.id,
#             'category': b.category,
#             'professional_id': b.professional_id,
#             'professional': {
#                 'user': {
#                     'fname': b.professional.user.fname if b.professional and b.professional.user else "Unknown"
#                 }
#             },
#             'date': b.booking_date.strftime('%Y-%m-%d'),
#             'time_slot': b.time_slot,
#             'price': b.price,
#             'status': b.status
#         } for b in bookings
#     ]

#     return jsonify(results), 200


@customer.route("/customer/service-review/<int:request_id>", methods=["POST"])
@jwt_required()
def submit_review(request_id):
    """
    API for customers to submit reviews.
    """
    try:
        # Get customer ID from JWT token
        user_id = get_jwt_identity()

        # Check if user exists as a customer
        customer = Customer.query.filter_by(id=user_id).first()
        if not customer:
            return jsonify({"error": "Unauthorized. Only customers can submit reviews."}), 403

        # Validate request payload
        data = request.get_json()
        review_text = data.get("review")
        rating = data.get("rating")

        if rating is None or not (1 <= rating <= 5):
            return jsonify({"error": "Rating must be between 1 and 5."}), 400

        # Get the service request and ensure it belongs to the customer
        service_request = ServiceRequest.query.filter_by(id=request_id, customer_id=customer.id).first()
        if not service_request:
            return jsonify({"error": "Service request not found or does not belong to you."}), 404

        if not service_request.professional_id:
            return jsonify({"error": "No professional assigned to this service request."}), 400

        # Ensure the service request is completed before allowing reviews
        if service_request.service_status != "completed":
            service_request.service_status = "completed"
            service_request.payment_status = "Paid"

        # Check if the customer has already reviewed this service request
        if service_request.ratings is not None:
            return jsonify({"error": "You have already submitted a review for this service."}), 400

        # Update the service request with the review
        service_request.reviews = review_text
        service_request.ratings = rating
        service_request.date_of_completion = datetime.utcnow()

        # Commit changes to the database
        db.session.commit()

        return jsonify({
            "message": "Review submitted successfully.",
            "service_request": {
                "id": service_request.id,
                "reviews": service_request.reviews,
                "ratings": service_request.ratings,
                "date_of_completion": service_request.date_of_completion.strftime('%Y-%m-%d %H:%M:%S'),
                "service_status": service_request.service_status,
                "payment_status": service_request.payment_status
            }
        }), 201


    except Exception as e:
        return jsonify({"error": str(e)}), 500



@customer.route("/customer/bookings", methods=["GET"])
@jwt_required()
def get_bookings_by_customer():
    try:
        user_id = get_jwt_identity()
        customer = Customer.query.filter_by(id=user_id).first()
        
        if not customer:
            return jsonify({"error": "Unauthorized access."}), 401  # 401 for unauthorized

        bookings = Booking.query.filter_by(customer_id=customer.id).all()
        bookings_data = []

        for booking in bookings:
            print(f"DEBUG: Booking ID {booking.id} -> Payment: {booking.payment_status}, Rating: {booking.ratings}, Review: {booking.reviews}")  # ✅ Debugging
            
            bookings_data.append({
                "id": booking.id,
                "customer_id": booking.customer_id,
                "professional_id": booking.professional_id,
                "service_id": booking.service_id,
                "category": booking.category,
                "date": booking.booking_date.strftime('%Y-%m-%d'),
                "time_slot": booking.time_slot,
                "status": booking.status,
                "price": booking.price,
                "payment_status": booking.payment_status if booking.payment_status else "Not Available",
                "payment_method": booking.payment_method if booking.payment_method else "Not Provided",
                "ratings": booking.ratings if booking.ratings is not None else "Not Rated",
                "reviews": booking.reviews if booking.reviews else "No Review",
                "customer": {
                    "id": booking.customer.id if booking.customer else None,
                    "name": booking.customer.user.fname if booking.customer and booking.customer.user else "Unknown"
                } if booking.customer else None,
                "professional": {
                    "id": booking.professional.id if booking.professional else None,
                    "name": booking.professional.user.fname if booking.professional and booking.professional.user else "Unknown"
                } if booking.professional else None,
                "service": {
                    "id": booking.service.id if booking.service else None,
                    "name": booking.service.name if booking.service else "Unknown"
                } if booking.service else None
            })

        return jsonify(bookings_data), 200

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": "Internal Server Error"}), 500


# ✅ Edit Service Request
@customer.route('/service-request/<int:request_id>', methods=['PUT'])
def edit_service_request(request_id):
    data = request.json
    request_obj = ServiceRequest.query.get(request_id)
    if not request_obj:
        return jsonify({'error': 'Service request not found'}), 404
    
    request_obj.service_dateTime = data.get('service_dateTime', request_obj.service_dateTime)
    request_obj.service_status = data.get('service_status', request_obj.service_status)
    db.session.commit()
    
    return jsonify({'message': 'Service request updated successfully'})

# ✅ Edit Package Request
@customer.route('/package-request/<int:request_id>', methods=['PUT'])
def edit_package_request(request_id):
    data = request.json
    request_obj = ProfessionalPackageRequest.query.get(request_id)
    if not request_obj:
        return jsonify({'error': 'Package request not found'}), 404
    
    request_obj.status = data.get('status', request_obj.status)
    db.session.commit()
    
    return jsonify({'message': 'Package request updated successfully'})

# ✅ Edit Booking
@customer.route('/booking/<int:booking_id>', methods=['PUT'])
def edit_booking(booking_id):
    data = request.json
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    booking.booking_date = data.get('booking_date', booking.booking_date)
    booking.time_slot = data.get('time_slot', booking.time_slot)
    booking.status = data.get('status', booking.status)
    db.session.commit()
    
    return jsonify({'message': 'Booking updated successfully'})

# ✅ Cancel Service Request
@customer.route('/customer/service-requests/<int:requestId>', methods=['DELETE'])
def cancel_service_request(requestId):
    request_obj = ServiceRequest.query.get(requestId)
    if not request_obj:
        return jsonify({'error': 'Service request not found'}), 404
    
    request_obj.service_status = 'cancelled'
    db.session.commit()
    
    return jsonify({'message': 'Service/Package request cancelled successfully'})

# ✅ Cancel Booking
@customer.route('/customer/bookings/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    booking.status = 'cancelled'
    db.session.commit()
    
    return jsonify({'message': 'Booking cancelled successfully'})

