from django.db import models
GENDER_CHOICES = (
   ('MALE', 'Male'),
   ('FEMALE', 'Female')
)

class Doctor(models.Model):
    username = models.CharField(max_length=500)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=128)
    year = models.IntegerField()
    month = models.CharField(max_length=50)
    date = models.CharField(max_length= 50)
    specialities = models.CharField(max_length=1000)
    education = models.CharField(max_length=1000)
    hospitals = models.CharField(max_length=1000)
    rate = models.FloatField()
    email = models.EmailField(unique=True)
    #phone_no = models.CharField(max_length=20)
    description = models.TextField()
   # port = models.IntegerField()


class Patient(models.Model):
    username = models.CharField(max_length=500)
    email = models.EmailField(unique=True)
    year = models.IntegerField()
    month = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    gender = models.CharField(max_length=20)
    age = models.IntegerField()
    description = models.TextField()
    #port = models.IntegerField()


class Make_appointment(models.Model):
    doctorEmailId = models.EmailField()
    year = models.IntegerField()
    month = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    hr = models.IntegerField()
    min = models.IntegerField()
    problems = models.CharField(max_length=9000)


class Recharge_balance(models.Model):
    recharge_card = models.IntegerField(default=0)


class CreateReport(models.Model):
    year = models.IntegerField()
    month = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    content = models.CharField(max_length=10000)
    institute = models.CharField(max_length=1000)



class Validate_appointment(models.Model):
    appointment_id = models.CharField(max_length=20)
    year = models.IntegerField(null=True, blank=True)
    month = models.CharField(max_length=200,null=True, blank=True)
    date = models.CharField(max_length=200,null=True, blank=True)
    hr = models.IntegerField(null=True, blank=True)
    min = models.IntegerField(null=True, blank=True)
    changedatetime = models.CharField(default=False, max_length=10)

class CreateDrReport(models.Model):
    year = models.IntegerField()
    month = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    content = models.CharField(max_length=10000)
    institute = models.CharField(max_length=1000)
    patient = models.EmailField(max_length=500)


class CreatePrescription(models.Model):
    diagnosis = models.CharField(max_length=20000)
    medications = models.CharField(max_length=10000)
    patient = models.EmailField(max_length=100)


 




































# # Create your models here.
# class Custom_doctor(AbstractUser):
#     gender = models.CharField(max_length=50)
#     year = models.IntegerField()
#     month = models.CharField(max_length=50)
#     date = models.CharField(max_length= 50)
#     specialities = models.CharField(max_length=1000)
#     education = models.CharField(max_length=1000)
#     hospitals = models.CharField(max_length=1000)
#     rate = models.FloatField()
#     email = models.EmailField(unique=True)
#     phone_no = models.CharField(max_length=20)
#
#
