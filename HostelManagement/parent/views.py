from django.shortcuts import render
import os
import sys
import socket
import io
import selectors

# Create your views here.
def load_index(request):
   # id =request.session.get('userid')
   # user = student.objects.get(sd_id=id)
    return render(request,'parent_templates/index.html')
def contact(request):
    return render(request,'parent_templates/contact.html')