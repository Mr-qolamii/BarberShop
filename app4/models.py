from django.db.models.signals import m2m_changed
from django.utils.datetime_safe import datetime
from django.dispatch.dispatcher import receiver
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Product(models.Model):
    file1 = models.FileField(upload_to='products')
    file2 = models.FileField(upload_to='products')
    file3 = models.FileField(upload_to='products')
    file4 = models.FileField(upload_to='products')
    file5 = models.FileField(upload_to='products')
    file6 = models.FileField(upload_to='products')
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[(1, 'machine'), (2, 'kif vasayel'), (3, 'arayeshi behdashti')])
    price = models.IntegerField()
    SoldOut = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)


class SoldOut(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
