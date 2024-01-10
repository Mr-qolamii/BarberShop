from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import validate_international_phonenumber
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.db import models
from phonenumbers.unicode_util import Category


class UserManager(BaseUserManager):
    """this is class manager for user model """

    def _create_user(self, username, tell, password, **extra_fields):
        """ create user """
        tell = validate_international_phonenumber(tell)
        user = self.model(username=username, tell=tell, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, tell, password, **extra_field):

        return self._create_user(username, tell, password, **extra_field)

    def create_super_user(self, username, tell, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)

        return self._create_user(username, tell, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """this is class for user model """

    username = models.CharField(max_length=25, unique=True)
    tell = PhoneNumberField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"

    objects = UserManager()

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="profiles")
    profile_pic = models.ImageField()
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    age = models.DateField()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
