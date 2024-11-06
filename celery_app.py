from celery import Celery

# Use the service name 'redis' from docker-compose as the hostname
app = Celery('my_app', broker='redis://redis:6379/0')

# Optionally, specify result backend if needed
app.conf.update(
    result_backend='redis://redis:6379/0'
)

