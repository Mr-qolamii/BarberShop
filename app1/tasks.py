from celery import Celery

from .models import *

app = Celery("app1_tasks", backend='redis://localhost:6379', broker='redis://localhost:6379')


@app.task
def send_sms(tell: str, msg: str) -> None:
    # api send sms to (tell)
    message = f""" 
    reset password link
    {msg}
    """


@app.task
def create_user(username: str, tell: str, password: str, **extra_field) -> None:
    User.objects.create_user(username=username, tell=tell, password=password, **extra_field)


if __name__ == "__main__":
    app.start()
