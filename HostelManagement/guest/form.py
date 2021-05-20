from .models import *
from django import forms

class GuestRegister(forms.ModelForm):
    class Meta:
        model = register_guest
        fields = ['name', 'admno', 'phone', 'email', 'course','year',  'sdate', 'ldate', 'days','room']