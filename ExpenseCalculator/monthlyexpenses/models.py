from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Source(models.Model):
    label = models.CharField(max_length=30)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    profile_photo = models.FileField(upload_to="profiles/")
