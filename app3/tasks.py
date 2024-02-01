from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from core.celery import app
from .models import *


@app.task
def create_reserve(**kwargs):
    return Reservation.objects.create(**kwargs)
