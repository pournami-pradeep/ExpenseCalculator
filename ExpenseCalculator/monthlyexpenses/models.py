from django.db import models

# Create your models here.

class Source(models.Model):
    label = models.CharField(max_length=30)
