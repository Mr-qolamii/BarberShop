import os

from core.celery import app
from .models import *


@app.task
def send_sms(tell: str, msg: str) -> None:
    # api send sms to (tell)
    message = f""" 
    reset password link
    {msg}
    """
    print(message)


@app.task
def create_user(username: str, tell: str, password: str, **extra_field) -> None:
    User.objects.create_user(username=username, tell=tell, password=password, **extra_field)


if __name__ == "__main__":
    app.start()
