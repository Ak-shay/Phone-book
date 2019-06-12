from django.db import models
from django.contrib.auth.models import AbstractUser
from validators.phone_validator import validate_phone
from django.conf import settings


class CustomUser(AbstractUser):

    age = models.PositiveSmallIntegerField()
    phone = models.CharField(max_length=10, validators=[validate_phone], unique=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'age', 'username']

    def __unicode__(self):
        return self.phone
