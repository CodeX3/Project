from django.db import models

# Create your models here.
class register_guest(models.Model):
    name=models.CharField(max_length=50)
    admno=models.CharField(max_length=10)
    phone=models.CharField(max_length=10)
    email=models.CharField(max_length=128)
    course=models.CharField(max_length=40)
    year=models.CharField(max_length=4)
    sdate=models.DateField()
    ldate=models.DateField()
    days=models.IntegerField()
    room=models.IntegerField(default=0)
    status=models.BooleanField(default=True)




