from django.db import models


# Create your models here.
class register_new_user(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    course = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    admno = models.CharField(max_length=10)


class contact_us(models.Model):
    uname = models.CharField(max_length=20)
    uemail = models.CharField(max_length=50)
    uphone = models.CharField(max_length=10)
    umsg = models.CharField(max_length=250)


class student(models.Model):
    sd_id = models.AutoField(primary_key=True)
    sd_name = models.CharField(max_length=50)
    sd_admno = models.CharField(max_length=10)
    sd_course = models.CharField(max_length=50)
    sd_year = models.CharField(max_length=4)
    sd_dob = models.DateField()
    sd_email = models.CharField(max_length=100)
    sd_guardian = models.CharField(max_length=30)
    sd_address = models.CharField(max_length=100)
    sd_phone = models.CharField(max_length=20)
    sd_guardian_phone = models.CharField(max_length=20)
    sd_room_no = models.CharField(max_length=999)
    sd_feedback = models.CharField(max_length=150, null=True)
    sd_remark = models.CharField(max_length=150, null=True)
    sd_fees = models.CharField(max_length=50000, null=True)
    sd_university_register = models.CharField(max_length=50, null=True)
    sd_parent = models.CharField(max_length=150)
    sd_parent_phone = models.CharField(max_length=20)
    sd_password = models.CharField(max_length=250)
    sd_pic = models.ImageField(upload_to='student_profile_pic', default='student.jpg')


class visitor(models.Model):
    visitor_name = models.CharField(max_length=100)
    visitor_contact = models.CharField(max_length=100)
    visitor_student_id = models.CharField(max_length=1000)
    visitor_student_name = models.CharField(max_length=50)
    visitor_date = models.DateField(null=True)
    visitor_count = models.IntegerField(default=1)
    reg_day = models.DateField(null=True)


class complaint(models.Model):
    auther = models.CharField(max_length=50)
    auther_phone = models.CharField(max_length=20)
    auther_ID = models.CharField(max_length=1000)
    subject = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    date = models.DateField()
    body = models.CharField(max_length=500)


class attendance(models.Model):
    sd_id = models.IntegerField()
    date = models.DateField(null=True)
    month = models.CharField(max_length=31)
    year = models.CharField(max_length=5000)
    status = models.BooleanField(default=False)
    sd_name = models.CharField(max_length=50)
    stduent_info = models.ForeignKey(student, on_delete=models.CASCADE, null=True)


class fees(models.Model):
    sd_id = models.IntegerField()
    created_date = models.DateField()
    status = models.BooleanField(default=False)
    month = models.IntegerField()
    year = models.IntegerField()
    paid_by = models.CharField(max_length=50, null=True)
    transaction = models.CharField(max_length=100, null=True)
    mess_fee = models.IntegerField(null=True)
    fine = models.IntegerField(null=True)
    accommodation = models.IntegerField(null=True)
    common = models.IntegerField(null=True)
    total = models.IntegerField()
    orderid = models.CharField(max_length=200, null=True)
    amount_paise = models.IntegerField(null=True)
    student_info = models.ForeignKey(student, on_delete=models.CASCADE, null=True)


class warden(models.Model):
    name = models.CharField(max_length=50)
    is_main = models.BooleanField(default=False)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    status = models.BooleanField(default=True)
    is_normal = models.BooleanField(default=True)
    incharge = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    pic = models.ImageField(upload_to='admin_profile_pic', default='default.jpg')


class marks(models.Model):
    sd_id = models.IntegerField()
    sd_name = models.CharField(max_length=50)
    sd_admno = models.CharField(max_length=10)
    mark1 = models.IntegerField(default=0)
    mark2 = models.IntegerField(default=0)
    total = models.IntegerField()


class Razorpay(models.Model):
    razorpay_payment_id = models.CharField(max_length=250)
    razorpay_order_id = models.CharField(max_length=250)
    razorpay_signature = models.CharField(max_length=250)
    fee_info = models.ForeignKey(fees, on_delete=models.CASCADE)


class leave(models.Model):
    sd_id = models.IntegerField()
    student_info = models.ForeignKey(student, on_delete=models.CASCADE)
    sd_name = models.CharField(max_length=50)
    leave_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=250)
    half_day = models.BooleanField(default=False)
    no_of_day = models.IntegerField(default=1)


class service(models.Model):
    auther = models.CharField(max_length=50)
    auther_phone = models.CharField(max_length=20)
    auther_ID = models.CharField(max_length=1000)
    subject = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    date = models.DateField()
    body = models.CharField(max_length=500, null=True)
    important = models.BooleanField(default=False)
    closed = models.DateField(null=True)


class notification(models.Model):
    name = models.CharField(max_length=50)
    msg = models.CharField(max_length=100)
    pic = models.ImageField(blank=True,null=True)
    date = models.DateField()
    time = models.CharField(max_length=10)
    temp = models.CharField(max_length=50,null=True)
    status = models.BooleanField(default=True)

class mess_menu(models.Model):
    day = models.CharField(max_length=20)
    mng = models.CharField(max_length=30)
    noon = models.CharField(max_length=30)
    night = models.CharField(max_length=30)

class FoodWaste(models.Model):
    day = models.CharField(max_length=15)
    Bake = models.CharField(max_length=10)
    Consumed = models.CharField(max_length=10)