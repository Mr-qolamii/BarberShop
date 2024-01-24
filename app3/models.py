from django.contrib.auth import get_user_model
from django.db import models


class Reservation(models.Model):
    """ reservation model """
    choices = [(1, "فید"),
               (2, "هیر کات مدرن"),
               (3, "پاکسازی"),
               (4, "پاکسازی و استایل"),
               (5, "فید و پاکسازی"),
               (6, "فید و هریکات"),
               (7, "فید و میکاپ"),
               (8, "فید و پاکسازی و میکاپ"),
               (9, "فید و استایل و میکاپ"),
               (10, "فید و استایل و پاکسازی"),
               (11, "فید و استایل و میکاپ و پاکسازی"),
               ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.BooleanField(default=True)
    content = models.CharField(max_length=30, choices=choices)


