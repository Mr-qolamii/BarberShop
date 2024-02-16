from core.celery import app
from .models import *


@app.task
def create_comment(**kwargs):
    return Comment.objects.create(**kwargs)


@app.task
def post_view(**kwargs):
    return PostViews.objects.create(**kwargs)


@app.task
def post_like(**kwargs):
    return PostLike.objects.create(**kwargs)


@app.task
def post_like_delete(**kwargs):
    return PostLike.objects.get(**kwargs).delete()

