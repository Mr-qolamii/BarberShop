from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import validate_international_phonenumber
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models


class UserManager(BaseUserManager):
    """this is class manager for user model """

    def _create_user(self, username, tell, password, **extra_fields):
        """ create user """
        tell = validate_international_phonenumber(tell)
        user = self.model(username=username, tell=tell, password=password, **extra_fields)
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
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    tell = PhoneNumberField(unique=True)
    age = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"

    objects = UserManager()

    def __str__(self):
        return self.username
