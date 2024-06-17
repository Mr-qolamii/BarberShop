from django.db.models.signals import m2m_changed, post_save
from django.utils.datetime_safe import datetime
from django.dispatch.dispatcher import receiver
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Product(models.Model):
    file1 = models.FileField(upload_to='products', blank=True)
    file2 = models.FileField(upload_to='products', blank=True)
    file3 = models.FileField(upload_to='products', blank=True)
    file4 = models.FileField(upload_to='products', blank=True)
    file5 = models.FileField(upload_to='products', blank=True)
    file6 = models.FileField(upload_to='products', blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[(1, 'machine'), (2, 'kif vasayel'), (3, 'arayeshi_behdashti')])
    price = models.IntegerField()
    count = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    is_done = models.BooleanField(default=False)




