from django.db import models

# Create your models here.
class register_new_user(models.Model):
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=128)
    fname=models.CharField(max_length=30)
    lname=models.CharField(max_length=30)
    phone=models.CharField(max_length=10)
    address=models.CharField(max_length=100)
    course=models.CharField(max_length=50)
    year=models.CharField(max_length=4)
    admno=models.CharField(max_length=10)

class contact_us(models.Model):
    uname=models.CharField(max_length=20)
    uemail=models.CharField(max_length=50)
    uphone=models.CharField(max_length=10)
    umsg=models.CharField(max_length=250)

class student(models.Model):
    sd_id=models.AutoField(primary_key=True)
    sd_name=models.CharField(max_length=50)
    sd_admno=models.CharField(max_length=10)
    sd_course=models.CharField(max_length=50)
    sd_year=models.CharField(max_length=4)
    sd_dob=models.DateField()
    sd_email=models.CharField(max_length=100)
    sd_guardian=models.CharField(max_length=30)
    sd_address=models.CharField(max_length=100)
    sd_phone=models.CharField(max_length=20)
    sd_guardian_phone=models.CharField(max_length=20)
    sd_room_no=models.CharField(max_length=999)
    sd_feedback=models.CharField(max_length=150,null=True)
    sd_remark=models.CharField(max_length=150,null=True)
    sd_fees=models.CharField(max_length=50000,null=True)
    sd_university_register=models.CharField(max_length=50,null=True)
    sd_parent=models.CharField(max_length=150)
    sd_parent_phone=models.CharField(max_length=20)
    sd_password=models.CharField(max_length=250)

class visitor(models.Model):
    visitor_name=models.CharField(max_length=100)
    visitor_contact=models.CharField(max_length=100)
    visitor_student_id=models.CharField(max_length=1000)