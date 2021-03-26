from .models import *
from django import forms


class Register(forms.ModelForm):
    class Meta:
        model = register_new_user
        fields = ['email', 'password', 'fname', 'lname', 'phone', 'address', 'course', 'year', 'admno']


class contact_us(forms.ModelForm):
    class Meta:
        model = contact_us
        fields = ['uname', 'uemail', 'uphone', 'umsg']
class Student_add(forms.ModelForm):
    class Meta:
        model = student
        fields =['sd_name','sd_admno','sd_course','sd_year','sd_dob','sd_email','sd_guardian','sd_address','sd_room_no','sd_phone','sd_guardian_phone','sd_parent','sd_parent_phone','sd_password']