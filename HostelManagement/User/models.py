from django.db import models

# Create your models here.
class register_new_user(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=128)
    fname=models.CharField(max_length=30)
    lname=models.CharField(max_length=30)
    phone=models.CharField(max_length=10)
    course=models.CharField(max_length=50)
    year=models.CharField(max_length=4)
    admno=models.CharField(max_length=10)
