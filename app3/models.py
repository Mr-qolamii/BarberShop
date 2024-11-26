from django.contrib.auth import get_user_model
from django.db import models


class Reservation(models.Model):
    """ reservation model """
    choices = [("فید", "فید"),
               ("هیر کات مدرن", "هیر کات مدرن"),
               ("پاکسازی", "پاکسازی"),
               ("پاکسازی و استایل", "پاکسازی و استایل"),
               ("فید و پاکسازی", "فید و پاکسازی"),
               ("فید و هریکات", "فید و هریکات"),
               ("فید و میکاپ", "فید و میکاپ"),
               ("فید و پاکسازی و میکاپ", "فید و پاکسازی و میکاپ"),
               ("فید و استایل و میکاپ", "فید و استایل و میکاپ"),
               ("فید و استایل و پاکسازی", "فید و استایل و پاکسازی"),
               ("فید و استایل و میکاپ و پاکسازی", "فید و استایل و میکاپ و پاکسازی"),
               ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, to_field='username')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField()
    is_canceled = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)

    contact = models.CharField(max_length=30, choices=choices)


