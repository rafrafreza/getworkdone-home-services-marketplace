from flask import Blueprint, request, jsonify, send_file
from backend.models import *
from flask_jwt_extended import jwt_required, get_jwt_identity
import io
import base64
import logging
from sqlalchemy import func

admin = Blueprint('admin', __name__)

# ✅ Get all pending professional verification requests
@admin.route('/admin/professionals/pending-requests', methods=['GET'])
def get_pending_professional_requests():
    pending_professionals = ServiceProfessional.query.filter_by(profile_verified=False).all()
    return jsonify([{'id': p.id, 
                     'name': p.user.fname, 
                     'email': p.email,
                     'service_type': p.service_type,
                     'experience': p.experience,
                     'city': p.city,
                     'price': p.base_price_per_hour,
                     } for p in pending_professionals])

# @admin.route('admin/resume/<int:professional_id>')
# def get_resume(professional_id):
#     professional = ServiceProfessional.query.get(professional_id)
#     if not professional or not professional.resume:
#         return jsonify({"message": "Resume not found"}), 404

#     pdf_data = base64.b64decode(professional.resume)
#     return send_file(io.BytesIO(pdf_data), mimetype='application/pdf', as_attachment=False, download_name="resume.pdf")




@admin.route('admin/resume/<int:request_id>')
def get_resume(request_id):
    professional = ServiceProfessional.query.get(request_id)
    if not professional or not professional.resume:
        return jsonify({"error": "Resume not found"}), 404

    resume_data = professional.resume.strip()


    # Remove 'data:application/pdf;base64,' if present
    if resume_data.startswith("data:application/pdf;base64,"):
        resume_data = resume_data.replace("data:application/pdf;base64,", "")

    try:
        pdf_data = base64.b64decode(resume_data)
    except Exception as e:
        logging.error(f"Decoding error: {e}")
        return jsonify({"error": "Invalid Base64 encoding"}), 400

    filename = f"professional_id_{professional.id}_resume.pdf"

    # Convert binary data to a downloadable PDF response
    return send_file(io.BytesIO(pdf_data), mimetype="application/pdf", as_attachment=True, download_name=filename)




# ✅ Approve a professional profile
@admin.route('/admin/professionals/approve/<int:id>', methods=['PUT'])
def approve_professional(id):
    professional = ServiceProfessional.query.get(id)
    if not professional:
        return jsonify({'error': 'Professional not found'}), 404
    professional.profile_verified = True
    db.session.commit()
    return jsonify({'message': 'Professional approved successfully'})

# ✅ Reject a professional profile
@admin.route('/admin/professionals/reject/<int:id>', methods=['PUT'])
def reject_professional(id):
    professional = ServiceProfessional.query.get(id)
    if not professional:
        return jsonify({'error': 'Professional not found'}), 404
    db.session.delete(professional)
    db.session.commit()
    return jsonify({'message': 'Professional rejected successfully'})


# ✅ Get all pending package requests
@admin.route('/admin/professionals/package-requests/pending', methods=['GET'])
def get_pending_package_requests():
    pending_requests = ProfessionalPackageRequest.query.filter_by(status='pending').all()
    
    response = []
    for req in pending_requests:
        professional = ServiceProfessional.query.get(req.professional_id)
        user = Users.query.get(professional.id) if professional else None  # Fetch associated user
        package = ServicePackage.query.get(req.package_id)

        response.append({
            'id': req.id,
            'professional_id': req.professional_id,
            'package_id': req.package_id,
            'prof_name': user.fname if user else None,  # Fetch first name from User table
            'service_type': professional.service_type if professional else None,
            'experience': professional.experience if professional else None,
            'city': professional.city if professional else None,
            'package_name': package.name if package else None,
            'package_type': package.package_type if package else None,
            'status': req.status
        })
    
    return jsonify(response)



# ✅ Approve a package request
@admin.route('/admin/professionals/package-requests/approve/<int:id>', methods=['PUT'])
def approve_package_request(id):
    request = ProfessionalPackageRequest.query.get(id)
    if not request:
        return jsonify({'error': 'Request not found'}), 404
    request.status = 'approved'
    db.session.commit()
    return jsonify({'message': 'Package request approved'})

# ✅ Reject a package request
@admin.route('/admin/professionals/package-requests/reject/<int:id>', methods=['PUT'])
def reject_package_request(id):
    request = ProfessionalPackageRequest.query.get(id)
    if not request:
        return jsonify({'error': 'Request not found'}), 404
    request.status = 'rejected'
    db.session.commit()
    return jsonify({'message': 'Package request rejected'})


# ✅ Fetch All Users
@admin.route('/admin/users', methods=['GET'])
def get_all_users():
    users = Users.query.all()
    user_list = []
    
    for user in users:
        if user.role != 2:  # Exclude Admins
            user_data = {
                'id': user.id,
                'phone': user.phone,
                'fname': user.fname,
                'role': 'Professional' if user.role == 1 else 'Customer',
                'blocked': user.customer.blocked if user.customer else user.service_professional.blocked if user.service_professional else False,
                'profile_picture': user.profile_picture
            }
            
            # If the user is a Professional, add additional details
            if user.role == 1 and user.service_professional:
                user_data.update({
                    'email': user.service_professional.email,
                    'service_type': user.service_professional.service_type,
                    'experience': user.service_professional.experience,
                    'profile_verified': user.service_professional.profile_verified,
                    'address': user.service_professional.address,
                    'pin_code': user.service_professional.pin_code,
                    'city': user.service_professional.city,
                    'base_price_per_hour': user.service_professional.base_price_per_hour,
                    'availability_slots': user.service_professional.availability_slots,
                    'resume': user.service_professional.resume
                })
            
            # If the user is a Customer, add additional details
            elif user.role == 0 and user.customer:
                user_data.update({
                    'address': user.customer.address,
                    'pin_code': user.customer.pin_code,
                    'city': user.customer.city
                })
            
            user_list.append(user_data)
    
    return jsonify(user_list)


# ✅ Block/Unblock User
@admin.route('/admin/users/block/<int:id>', methods=['PUT'])
def block_unblock_user(id):
    user = Users.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user.role == 0 and user.customer:
        user.customer.blocked = not user.customer.blocked
    elif user.role == 1 and user.service_professional:
        user.service_professional.blocked = not user.service_professional.blocked
    else:
        return jsonify({'message': 'Admin cannot be blocked'}), 400

    db.session.commit()
    return jsonify({'message': 'User status updated'})

# ✅ Delete User
@admin.route('/admin/users/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = Users.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    ServiceRequest.query.filter_by(customer_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'})





# --------------------------------
# ✅ EDIT CATEGORY
# --------------------------------
@admin.route('/categorys/<int:id>', methods=['PUT'])
def edit_category(id):
    category = ServiceCategory.query.get(id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    data = request.json
    if 'name' in data:
        category.name = data['name']
    if 'picture' in data:
        category.picture = data['picture']

    db.session.commit()
    return jsonify({'message': 'Category updated successfully', 'category': {
        'id': category.id, 'name': category.name, 'picture': category.picture
    }})

# --------------------------------
# ✅ DELETE CATEGORY
# --------------------------------
@admin.route('/categorys/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = ServiceCategory.query.get(id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted successfully'})

# --------------------------------
# ✅ EDIT SERVICE
# --------------------------------
@admin.route('/services/<int:id>', methods=['PUT'])
def edit_service(id):
    service = Service.query.get(id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    data = request.json
    if 'name' in data:
        service.name = data['name']
    if 'base_price' in data:
        service.base_price = data['base_price']
    if 'time_required' in data:
        service.time_required = data['time_required']
    if 'description' in data:
        service.description = data['description']
    if 'category_id' in data:
        service.category_id = data['category_id']

    db.session.commit()
    return jsonify({'message': 'Service updated successfully', 'service': {
        'id': service.id, 'name': service.name, 'base_price': service.base_price,
        'time_required': service.time_required, 'description': service.description
    }})

# --------------------------------
# ✅ DELETE SERVICE
# --------------------------------
@admin.route('/services/<int:id>', methods=['DELETE'])
def delete_service(id):
    service = Service.query.get(id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Service deleted successfully'})

# --------------------------------
# ✅ EDIT SERVICE PACKAGE
# --------------------------------
@admin.route('/packages/<int:id>', methods=['PUT'])
def edit_package(id):
    package = ServicePackage.query.get(id)
    if not package:
        return jsonify({'error': 'Package not found'}), 404

    data = request.json
    if 'name' in data:
        package.name = data['name']
    if 'description' in data:
        package.description = data['description']
    if 'base_price' in data:
        package.base_price = data['base_price']
    if 'time_required' in data:
        package.time_required = data['time_required']
    if 'picture' in data:
        package.picture = data['picture']
    if 'package_type' in data:
        package.package_type = data['package_type']
    if 'category_id' in data:
        package.category_id = data['category_id']

    db.session.commit()
    return jsonify({'message': 'Package updated successfully', 'package': {
        'id': package.id, 'name': package.name, 'base_price': package.base_price,
        'time_required': package.time_required, 'description': package.description
    }})

# --------------------------------
# ✅ DELETE SERVICE PACKAGE
# --------------------------------
@admin.route('/packages/<int:id>', methods=['DELETE'])
def delete_package(id):
    package = ServicePackage.query.get(id)
    if not package:
        return jsonify({'error': 'Package not found'}), 404

    db.session.delete(package)
    db.session.commit()
    return jsonify({'message': 'Package deleted successfully'})





@admin.route('/admin/serv_pack_req', methods=['GET'])
def get_all_service_requests():
    try:
        service_requests = ServiceRequest.query.all()
        requests_list = [
            {
                "id": req.id,
                "service_name": req.service.name if req.service else "Package Service",
                "customer_name": req.customer.user.fname if req.customer and req.customer.user else "Unknown",
                "professional_name": req.professional.user.fname if req.professional and req.professional.user else "Not Assigned",
                "service_dateTime": req.service_dateTime.strftime("%Y-%m-%d %H:%M"),
                "date_of_request": req.date_of_request.strftime("%Y-%m-%d"),
                "date_of_completion": req.date_of_completion.strftime("%Y-%m-%d") if req.date_of_completion else "Not Completed",
                "service_status": req.service_status,
                "payment_status": req.payment_status,
                "ratings": req.ratings if req.ratings else "No Rating",
                "reviews": req.reviews if req.reviews else "No Review",
            }
            for req in service_requests
        ]
        return jsonify({"success": True, "service_requests": requests_list})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@admin.route('/admin/all-bookings-info', methods=['GET'])
@jwt_required()
def get_all_bookings():
    current_user_id = get_jwt_identity()
    admin = Users.query.filter_by(id=current_user_id, role=2).first()

    if not admin:
        return jsonify({"error": "Unauthorized"}), 403  # Only admins can access

    bookings = Booking.query.all()
    
    bookings_data = []
    for booking in bookings:
        bookings_data.append({
            "id": booking.id,
            "customer": booking.customer.user.fname,
            "professional": booking.professional.user.fname,
            "category": booking.category,
            "booking_date": booking.booking_date.strftime('%Y-%m-%d'),
            "time_slot": booking.time_slot,
            "price": booking.price,
            "status": booking.status,
            "payment_status": booking.payment_status
        })

    return jsonify({"bookings": bookings_data}), 200


@admin.route('/admin/stats', methods=['GET'])
def get_admin_stats():
    # total_users = db.session.query(func.count(Users.id)).scalar()
    total_professionals = db.session.query(func.count(ServiceProfessional.id)).scalar()
    total_customers = db.session.query(func.count(Customer.id)).scalar()
    total_services = db.session.query(func.count(Service.id)).scalar()
    total_bookings = db.session.query(func.count(Booking.id)).scalar()
    total_requests = db.session.query(func.count(ServiceRequest.id)).scalar()

    return jsonify({
        # "total_users": total_users-1,
        "total_professionals": total_professionals,
        "total_customers": total_customers,
        "total_services": total_services,
        "total_bookings": total_bookings,
        "total_requests": total_requests
    })


@admin.route('/admin/bookings-per-category', methods=['GET'])
def bookings_per_category():
    data = db.session.query(
        Booking.category, func.count(Booking.id)
    ).group_by(Booking.category).all()

    result = {category: count for category, count in data}
    
    return jsonify(result)



@admin.route('/admin/service-request-status', methods=['GET'])
def service_request_status():
    data = db.session.query(
        ServiceRequest.service_status, func.count(ServiceRequest.id)
    ).group_by(ServiceRequest.service_status).all()

    result = {status: count for status, count in data}

    return jsonify(result)


@admin.route('/admin/recent-bookings', methods=['GET'])
def recent_bookings():
    data = Booking.query.order_by(Booking.booking_date.desc()).limit(5).all()

    result = [
        {
            "id": booking.id,
            "customer": booking.customer_id,
            "professional": booking.professional_id,
            "category": booking.category,
            "date": booking.booking_date.strftime('%Y-%m-%d'),
            "price": booking.price,
            "status": booking.status
        }
        for booking in data
    ]

    return jsonify(result)




@admin.route('/admin/top-professionals', methods=['GET'])
def top_professionals():
    data = db.session.query(
        Booking.professional_id, func.count(Booking.id)
    ).group_by(Booking.professional_id).order_by(func.count(Booking.id).desc()).limit(5).all()

    result = [{"professional_id": prof_id, "bookings": count} for prof_id, count in data]

    return jsonify(result)


@admin.route('/admin/top-customers', methods=['GET'])
def top_customers():
    data = db.session.query(
        Booking.customer_id, func.count(Booking.id)
    ).group_by(Booking.customer_id).order_by(func.count(Booking.id).desc()).limit(5).all()

    result = [{"customer_id": cust_id, "bookings": count} for cust_id, count in data]

    return jsonify(result)
