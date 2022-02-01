import datetime

from django.db import models


# Create your models here.
class User(models.Model):
    mob = models.CharField(max_length=14, primary_key=True)
    eid = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)


class Log(models.Model):
    logtime = models.DateTimeField(primary_key=True)
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    mask = models.BooleanField()
    temp = models.DecimalField(decimal_places=3,max_digits=5)
    access = models.BooleanField()