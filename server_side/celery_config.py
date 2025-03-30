broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/1"
Timezone = "Asia/kolkata"
broker_connection_retry_on_startup = True


# Celery Beat configuration
beat_schedule = {}  # We will define tasks dynamically