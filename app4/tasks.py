
from .models import *
from core import app


@app.task
def create_order(**kwargs):
    return Order.objects.create(**kwargs)