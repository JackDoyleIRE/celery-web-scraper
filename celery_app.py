import os
from dotenv import load_dotenv
from celery import Celery
import tasks

# Load environment variables from .env file
load_dotenv()

# Check if we're in a Docker environment or running locally
broker_url = os.getenv("CELERY_BROKER_URL", os.getenv("LOCAL_CELERY_BROKER_URL"))
backend_url = os.getenv("CELERY_BACKEND_URL", os.getenv("LOCAL_CELERY_BACKEND_URL"))

app = Celery("my_app", broker=broker_url)
app.conf.update(result_backend=backend_url)

# Automatically discover tasks in modules named 'tasks'
app.autodiscover_tasks(['tasks'])

