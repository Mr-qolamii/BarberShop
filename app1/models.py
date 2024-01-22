from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import validate_international_phonenumber
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.db import models


class UserManager(BaseUserManager):
    """this is class manager for user model """

    def _create_user(self, username, tell, password, **extra_fields):
        """ create user """
        if validate_international_phonenumber(tell) is None:
            user = self.model(username=username, tell=tell, **extra_fields)
            user.set_password(password)
            user.save()
            return user
        raise ValidationError("Invalid phone number")

    def create_user(self, username, tell, password, **extra_field):

        return self._create_user(username, tell, password, **extra_field)

    def create_superuser(self, username, tell, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)

        return self._create_user(username, tell, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """this is class for user model """

    username = models.CharField(max_length=25, unique=True)
    tell = PhoneNumberField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["tell"]

    objects = UserManager()

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="profiles")
    profile_pic = models.ImageField(default="image/profile_pic/default.jpg", upload_to="image/profile_pic/")
    firstname = models.CharField(max_length=25, blank=True, null=True)
    lastname = models.CharField(max_length=25, blank=True, null=True)
    age = models.DateField(blank=True, null=True)


class Device(models.Model):
     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="Devices")
     device_name = models.CharField(max_length=40)
     login_time = models.DateTimeField(auto_now_add=True)
     is_active = models.BooleanField()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
