from django.contrib.auth import get_user_model
from django.db import models


class Reservation(models.Model):
    """ reservation model """
    choices = [(1, ""),
               (2, ""),
               (3, ""),
               (4, ""),
               (5, ""),
               (6, ""),
               (7, ""),
               (8, ""),
               (9, ""),
               (10, ""),
               (11, ""),
               (12, ""),
               (13, "")]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateTimeField()
    content = models.CharField(choices=choices)


class CancelledReservation(models.Model):
    """ cancelled reservation model """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    date = models.DateTimeField()
