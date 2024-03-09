from random import randint
from kavenegar import KavenegarAPI, APIException, HTTPException
from django.conf import settings

from core import celery
from core.celery import app
from .models import *


@app.task
def send_sms(request, tell: str, ) -> None:
    # api send sms to (tell)
    code = randint(1043, 9781)

    api_key = settings.KAVENEGAR_API_KEY
    try:
        api = KavenegarAPI(api_key)
        params = {
            'receptor': tell,
            'message':  f""" reset password code: \n {code}""",
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        raise e
    except HTTPException as e:
        raise e


@app.task
def create_user(username: str, tell: str, password: str, **extra_field) -> None:
    return User.objects.create_user(username=username, tell=tell, password=password, **extra_field)