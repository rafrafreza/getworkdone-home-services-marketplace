from backend import create_app
from backend.models import db
from flask_cors import CORS  # Import CORS
from backend.celery_init import celery_init_app
from celery.schedules import crontab
import backend.tasks
app = create_app()
CORS(app)  
celery = celery_init_app(app)

# Schedule tasks using Celery Beat
celery.conf.beat_schedule = {
    "send_monthly_report": {
        "task": "Professional_Monthly_activity_report",
        # "schedule": crontab(day_of_month=1, hour=9, minute=0),  # Runs on 1st of every month at 9 AM
        "schedule": crontab(minute="*/2"),  # Runs every minute
    },
    "send_pending_requests_reminder": {
        "task": "pending_requests",
        # "schedule": crontab(hour=9, minute=0),  # Runs daily at 9 AM
        "schedule": crontab(minute="*/2"),  # Runs every minute
    },
}

if __name__ == '__main__':
    app.run(debug = True)