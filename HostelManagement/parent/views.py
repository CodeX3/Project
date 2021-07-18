from django.shortcuts import render
import os
import sys
import socket
import io
import selectors
from parent.decorators import *
# Create your views here.

@parentOnly
def load_index(request):
   # id =request.session.get('userid')
   # user = student.objects.get(sd_id=id)

    return render(request,'parent_templates/index.html')

@parentOnly
def load_student_profile(request):
    return render(request,'parent_templates/profile.html')
