from core.celery import app
from .models import *


@app.task
def create_reserve(**kwargs):
    return Reservation.objects.create(**kwargs)
