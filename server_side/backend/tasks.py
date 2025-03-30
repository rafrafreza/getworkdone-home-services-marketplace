from flask import render_template
from celery import shared_task
from backend.mail import mail
from datetime import datetime
from flask_mail import Message
import time
import csv
import os
from .models import *
#tasks .. 
# functions

STATIC_DIR = "backend/static"  # Ensure this directory exists

@shared_task(ignore_results=False, name="Admin_export_allServices_CSV_report")
def csv_report_by_admin():
    print("Report generating....😊😊😊")
    try:
        # Ensure directory exists
        if not os.path.exists(STATIC_DIR):
            os.makedirs(STATIC_DIR)

        # Fetch all ServiceRequests
        service_requests = ServiceRequest.query.all()

        # Define file path
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = f"SR_Report_{timestamp}.csv"
        file_path = os.path.join(STATIC_DIR, csv_filename)

        # Write to CSV
        with open(file_path, mode="w", newline="") as csv_file:
            report = csv.writer(csv_file)
            report.writerow(["ServiceID", "Customer", "Professional", "Category", "Date&Time", "Status", "Ratings", "Reviews"])

            for request in service_requests:
                report.writerow([
                    request.id,
                    request.customer.user.fname,
                    request.professional.user.fname if request.professional_id else "Not Assigned Yet",
                    request.service.name if request.service else request.package,  
                    request.service_dateTime,
                    request.service_status,
                    request.ratings if request.ratings else "No Rating",
                    request.reviews if request.reviews else "No Reviews"
                ])

        print(f"Report saved at: {file_path}")
        return csv_filename  # ✅ Only return filename, not full path

    except Exception as e:
        print(f"Error generating report: {str(e)}")
        return None  # ✅ Ensure it returns None if there’s an error


# @shared_task(ignore_results = False, name = "Customer_Monthly_activity_report")
# def custo_month_report():
#     customers = Customer.query.all()
#     ServiceRequest = ServiceRequest.query.filter_by(customer_id = customers.id).all()

#     for csr in ServiceRequest:


#     return "Customer Monthly Activity report"

@shared_task(ignore_results=False, name="Professional_Monthly_activity_report")
def prof_month_report():
    print("Sending Monthly Report....📌📌📌")
    try:
        professionals = ServiceProfessional.query.all()
        
        for professional in professionals:
            service_requests = ServiceRequest.query.filter_by(professional_id=professional.id).all()

            completed_services = len([req for req in service_requests if req.service_status == "completed"])
            pending_services = len([req for req in service_requests if req.service_status == "assigned"])

            # if completed_services == 0 and pending_services == 0:
            #     continue  # Skip sending email if no service data

            # Render email template with data
            email_html = render_template(
                "prof_monthly_report.html",
                professional_name=professional.user.fname,
                completed_services=completed_services,
                pending_services=pending_services,
                dashboard_link="http://127.0.0.1:5173/login"
            )

            # Create email message
            msg = Message(
                "Your Monthly Service Activity Report",
                sender="rezakne55@gmail.com",
                recipients=[professional.email]
            )
            msg.html = email_html  # Set HTML content

            # Send email
            mail.send(msg)

        return "Monthly Service Activity Reports sent successfully"

    except Exception as e:
        print(f"Error sending professional monthly report: {str(e)}")
        return None

# @shared_task(ignore_results = False, name = "Service_req_accepted")
# def req_status():
#     return "Your Service Request accepted and professional has been assigned Scuccessfully!!!"

@shared_task(ignore_results = False, name = "pending_requests")
def pending_req():
    print("Sending Daily Reminder....📌📌📌")
    professionals = ServiceProfessional.query.all()

    for professional in professionals:
        pending_requests = ServiceRequest.query.filter_by(service_status = "requested").all()

        if pending_requests:
            email_html = render_template(
                "Prof_notify_pending_req.html",
                professional_name=professional.user.fname,
                pending_count=len(pending_requests),
                dashboard_link="http://127.0.0.1:5173/login"
            )

            msg = Message(
                "Daily Reminder: Pending Service Requests",
                sender="rezakne55@gmail.com",
                recipients=[professional.email]
            )
            msg.html = email_html

            mail.send(msg)

    return "Pending Service Requests sent successfuly!!!"