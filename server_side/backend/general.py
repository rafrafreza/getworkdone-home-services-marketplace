from flask import Blueprint, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from backend.models import *
from backend.tasks import *
from celery.result import AsyncResult

general = Blueprint('general', __name__)

# ------------------------------
# ✅ Get Professionals data
# ------------------------------

@general.route('/all_professionals', methods=['GET'])
def get_all_professionals():
    professionals = ServiceProfessional.query.filter_by(profile_verified = True ).all()
    result = []  # This should remain a list

    for prof in professionals:
        result.append({  # Append each professional's data as a dictionary
            'id': prof.id,
            'name': prof.user.fname,
            'email': prof.email,
            'service_type': prof.service_type,
            'experience': prof.experience,
            'profile_verified': prof.profile_verified,
            'blocked': prof.blocked,
            'city': prof.city,
            'pin_code': prof.pin_code,
            'base_price_per_hour': prof.base_price_per_hour,
            'availability_slots': prof.availability_slots,
            'profile_picture': prof.user.profile_picture
        })

    return jsonify(result), 200  # Return a proper JSON response





#Backend Jobs

@general.route('/export_csv')
def export_csv():
    result = csv_report_by_admin.apply_async()
    return jsonify({"id": result.id})

@general.route('/csv_report/<id>')
def csv_report(id):
    res = AsyncResult(id)

    if res.ready() and res.result:  # Ensure task is complete and has a result
        return jsonify({"status": "ready", "file": res.result})  # Return filename

    return jsonify({"status": "pending"})

# ✅ New Route for Downloading the File
@general.route('/download_csv/<filename>')
def download_csv(filename):
    return send_from_directory('static', filename, as_attachment=True)

@general.route('/prof_monthly_report')
def p_monthly_report():
    result = prof_month_report.delay()
    return jsonify({
        "message": "Monthly report task has been started.",
        "task_id": result.id
    })

@general.route('/prof_mail_status/<task_id>')
def task_status(task_id):
    result = AsyncResult(task_id)
    return jsonify({
        "task_id": task_id,
        "status": result.status,  # e.g., PENDING, STARTED, SUCCESS, FAILURE
        "result": result.result if result.ready() else "Not available yet"
    })


@general.route('/prof_pending_req_notify')
def p_req_notify():
    result = pending_req.delay()
    return jsonify({
        "message": "Daily Reminder: Pending Service Requests",
        "task_id": result.id
    })