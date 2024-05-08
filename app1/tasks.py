from random import randint
from kavenegar import KavenegarAPI, APIException, HTTPException
from django.conf import settings

from core.celery import app
from .models import *


@app.task
def send_sms(tell: str, token: str) -> None:

    api_key = settings.KAVENEGAR_API_KEY
    try:
        api = KavenegarAPI(api_key)
        params = {
            'receptor': tell,
            'message': f""" reset password link: \n {token}""",
        }
        response = api.sms_send(params)
        return response
    except APIException as e:
        raise e
    except HTTPException as e:
        raise e


@app.task
def save_device(**kwargs):
    return Device.objects.create(**kwargs)


@app.task
def delete_device(**kwargs):
    return Device.objects.get(**kwargs).delete()


@app.task
def create_user(username: str, tell: str, password: str, **extra_field) -> None:
    return User.objects.create_user(username=username, tell=tell, password=password, **extra_field)
