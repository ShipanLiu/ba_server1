from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# now define own User Model and make the "email" field unique
class User(AbstractUser):
    email = models.EmailField(unique=True)

