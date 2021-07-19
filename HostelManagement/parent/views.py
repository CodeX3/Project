from datetime import date

from django.shortcuts import render, redirect
import os
import sys
import socket
import io
import selectors
import User.models
from parent.decorators import *
# Create your views here.


@parentOnly
def load_index(request):
   # id =request.session.get('userid')
   # user = student.objects.get(sd_id=id)

     return render(request,'parent_templates/index.html')
@parentOnly
def contact(request):
    all_warden = warden.objects.all()
    return render(request,'parent_templates/contact.html',{'obj': all_warden})

@parentOnly
def load_student_profile(request):
    id  = request.session.get("stdID")
    user = student.objects.get(sd_id=id)
    return render(request,'parent_templates/profile.html',{'user':user})

@parentOnly
def visitor_view(request):
    id = request.session.get("stdID")
    user = student.objects.get(sd_id=id)
    obj = visitor.objects.filter(visitor_student_id=id)

    return render(request,'parent_templates/visitor.html',{'obj':obj})

@parentOnly
def add_visitor(request):
    id = request.session.get('stdID')
    user = student.objects.get(sd_id=id)
    if request.method.upper() == "POST":
        obj = visitor()
        obj.visitor_name = request.POST['visitor_name']
        obj.visitor_contact = request.POST['visitor_contact']
        obj.visitor_student_id = user.sd_id
        obj.visitor_student_name = user.sd_name
        obj.visitor_date = request.POST['visitor_date']
        obj.reg_day = date.today().strftime("%Y-%m-%d")
        obj.visitor_count = request.POST['visitor_count']
        try:
            obj.save()
            redirect('parent')
        except Exception as e:
            redirect('parent_add_visitor')
    return render(request,'parent_templates/add_visitor.html')

@parentOnly
def payment_view(request):
    id = request.session.get("stdID")
    obj = fees.objects.filter(sd_id=id)
    return render(request,'parent_templates/all_fee.html',{'obj':obj})

def logout(request):
    request.session.flush()
    return redirect('parent_login')
@parentOnly
def list_parents(request):
    obj=  student.objects.all()
    return render(request,'parent_templates/parent.html',{'obj':obj})

@parentOnly
def add_complaint(request):
    id = request.session.get('stdID')
    user = student.objects.get(sd_id=id)

    if request.method == "POST":
        print(request.POST)
        try:
            reg = complaint()
            reg.auther = user.sd_parent
            reg.auther_phone = user.sd_parent_phone
            reg.auther_ID = user.sd_id
            reg.status = 'open'
            reg.date = request.POST['date']
            reg.subject = request.POST['subject']
            reg.body = request.POST['body']
            reg.save()
            return redirect('parent_complaints')
        except Exception as e:
            print(e)

    return render(request,'parent_templates/add_complaint.html',{'user':user})

@parentOnly
def complaints(request):
    id = request.session.get('stdID')
    user = student.objects.get(sd_id=id)
    obj = complaint.objects.filter(auther_ID=id)
    return render(request,'parent_templates/complaint.html',{'obj':obj})

@parentOnly
def mess(request):
    obj = mess_menu.objects.all()
    return render(request,'parent_templates/mess.html',{'obj':obj})