import os
from celery import Celery

from .models import *

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery("app1_tasks", backend='redis://localhost:6379', broker='redis://localhost:6379')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task
def send_sms(tell: str, msg: str) -> None:
    # api send sms to (tell)
    message = f""" 
    reset password link
    {msg}
    """


@app.task
def create_user(username: str, tell: str, password: str, **extra_field) -> None:
    return User.objects.create_user(username=username, tell=tell, password=password, **extra_field)


if __name__ == "__main__":
    app.start()
