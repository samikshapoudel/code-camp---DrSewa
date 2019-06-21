from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.



class Custom_patient(AbstractUser):
    email = models.EmailField(unique=True)
    year = models.IntegerField()
    month = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    gender = models.CharField(max_length=20)
    age = models.IntegerField()




class Make_appointment(models.Model):
    doctorEmailId = models.EmailField()
    year = models.IntegerField()
    month = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    hr = models.IntegerField()
    min = models.IntegerField()
    problems = models.CharField(max_length=9000)


class Recharge_balance(models.Model):
    recharge_card = models.IntegerField()


class CreateReport(models.Model):
    year = models.IntegerField()
    month = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    content = models.CharField(max_length=10000)
    institute = models.CharField(max_length=1000)










