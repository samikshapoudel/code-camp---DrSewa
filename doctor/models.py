from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Custom_doctor(AbstractUser):
    gender = models.CharField(max_length=50)
    year = models.IntegerField()
    month = models.CharField(max_length=50)
    date = models.CharField(max_length= 50)
    specialities = models.CharField(max_length=1000)
    education = models.CharField(max_length=1000)
    hospitals = models.CharField(max_length=1000)
    rate = models.FloatField()
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=20)


class Validate_appointment(models.Model):
    appointment_id = models.IntegerField()
    year = models.IntegerField()
    month = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    hr = models.IntegerField()
    min = models.IntegerField()
    changedatetime = models.BooleanField(default=False)

class CreateDrReport(models.Model):
    year = models.IntegerField()
    month = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    content = models.CharField(max_length=10000)
    institute = models.CharField(max_length=1000)
    patient = models.EmailField(max_length=500)





