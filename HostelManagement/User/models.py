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
    visitor_student_name=models.CharField(max_length=50)
    visitor_date=models.DateField(null=True)

class complaint(models.Model):
    auther=models.CharField(max_length=50)
    auther_phone=models.CharField(max_length=20)
    auther_ID=models.CharField(max_length=1000)
    subject=models.CharField(max_length=50)
    status=models.CharField(max_length=20)
    date=models.DateField()
    body=models.CharField(max_length=500)

class attendance(models.Model):
    sd_id=models.IntegerField()
    date=models.DateField(null=True)
    month =models.CharField(max_length=31)
    year =models.CharField(max_length=5000)
    status=models.BooleanField(default=False)
    sd_name=models.CharField(max_length=50)
    stduent_info=models.ForeignKey(student,on_delete=models.CASCADE,null=True)

class fees(models.Model):
    sd_id=models.IntegerField()
    created_date=models.DateField()
    status=models.BooleanField(default=False)
    month=models.IntegerField()
    year =models.IntegerField()
    paid_by=models.CharField(max_length=50,null=True)
    transaction=models.CharField(max_length=100,null=True)
    mess_fee=models.IntegerField(null=True)
    fine=models.IntegerField(null=True)
    accommodation=models.IntegerField(null=True)
    common=models.IntegerField(null=True)
    total=models.IntegerField()
    student_info =models.ForeignKey(student,on_delete=models.CASCADE,null=True)


