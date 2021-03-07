from .models import *
from django import  forms
class register(forms.ModelForm):
    class Meta:
        model = register_new_user
        fields=['email','password','fname','lname','phone','course','year','admno']

