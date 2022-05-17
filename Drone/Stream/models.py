from operator import mod
from statistics import mode
from django.db import models

# Create your models here.

class CBA(models.Model):
    class Meta:
        verbose_name_plural="CBA"
    user = models.CharField(max_length=1000)
    phoneNumber = models.IntegerField()
    emergencyValue = models.IntegerField()
    files = models.FileField()
    latitude = models.FloatField()
    longitude = models.FloatField()
