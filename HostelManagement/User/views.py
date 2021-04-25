import datetime
import json
from datetime import date
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.core.exceptions import *


# ---------------------------Login--------------------------------#
def do_login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        print("post request recieved")
        response = redirect('/test')
        return response


# ------------------------------USER ---------------------------------#
# 404 handler
def handler404(request, exception):
    return render(request, '404.html', locals())


def test(request):
    obj = register_new_user.objects.all()
    context = {'all_details': obj}
    return render(request, 'test.html', context)


def load_index(request):
    return render(request, 'index.html')


def do_register(request):
    if request.method == 'POST' and 'contact' in request.POST:
        form = contact_us(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            form = contact_us()
    if request.method == "POST" and 'submit' in request.POST:
        form = Register(request.POST)
        if form.is_valid():
            form.save()
            obj = {'status': True}
            return render(request, 'register_verification.html', obj)
        else:
            form = Register()
            obj = {'status': False}
            return render(request, 'register_verification.html', obj)
    return render(request, 'register.html')


# def load_contact(request):
#     if request.method =="POST" and 'contact' in request.POST:
#         print(request.body)
#         form =contact_us(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#         else:
#             form=contact_us()
#     obj = {'status': False}
#     return render(request,'register_verification.html',obj)


# ---------------------------Admin-------------------------------#

def load_admin_index(request):
    return render(request, 'admin_templates/index.html')


def verify_students(request):
    obj = register_new_user.objects.all()
    context = {'obj': obj}
    return render(request, 'admin_templates/student_reg_verify.html', context)


def verify_students_confirm(request, pk):
    obj = register_new_user.objects.get(id=pk)
    context = {'obj': obj}

    if request.method == "POST":
        form = Student_add(request.POST)

        if form.is_valid():
            form.save()
            obj.delete()
            return redirect('/dashboard/verification', {'alert': True})
        else:
            form = Student_add()

    return render(request, 'admin_templates/validate_student.html', context)


def table(request):
    return render(request, 'admin_templates/table.html')


def view_students(request):
    obj = student.objects.all()
    context = {'obj': obj}
    return render(request, 'admin_templates/student_view.html', context)


def edit_student(request, pk):
    obj = student.objects.get(sd_id=pk)
    context = {'obj': obj}

    if request.method == "POST":
        form = Student_edit(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/students')
        else:
            print("not valid")
    return render(request, 'admin_templates/edit_student.html', context)


def view_visitors(request):
    obj = visitor.objects.all()

    return render(request, 'admin_templates/visitor.html', {'obj': obj})


def view_complaints(request):
    obj = complaint.objects.all()

    return render(request, 'admin_templates/complaint.html', {'obj': obj})


def review_complaint(request):
    obj = complaint.objects.get(id=request.GET['id'])
    obj.status = "closed"
    obj.save()
    return HttpResponse(status=200)


def reg_complaint(request):
    if request.method == "POST":
        form = complaints(request.POST)
        if form.is_valid():
            form.save()
        else:
            form = complaints()
    return render(request, 'complaint_insert.html')


def today_attendance(request):
    today = date.today()
    obj = attendance.objects.filter(date=today).values("sd_id")
    res = [sub['sd_id'] for sub in obj]
    st_obj = student.objects.all()
    return render(request, 'admin_templates/today_attendance.html',
                  {'obj': st_obj, 'today': today, 'attendace_obj': res})


def mark_attendance(request):
    try:
        today = date.today().strftime("%Y-%m-%d")
        obj = attendance.objects.get(sd_id=request.GET['id'], date=today)
    except ObjectDoesNotExist:
        print(date.today().strftime("%Y-%m-%d"))
        obj = attendance()
        student_data = student.objects.get(sd_id=request.GET['id'])
        obj.status = 1
        obj.sd_id = request.GET['id']
        obj.date = date.today().strftime("%Y-%m-%d")
        obj.stduent_info = student_data
        obj.sd_name = student_data.sd_name
        obj.save()

    return HttpResponse(status=200)


def general_attendance(request):
    return render(request, 'admin_templates/category_view.html')


def date_attendance(request, date=None):
    if date is None:
        today = date.today().strftime("%Y-%m-%d")
        obj = attendance.objects.filter(date=today).values("sd_id")
        res = [sub['sd_id'] for sub in obj]
        st_obj = student.objects.all()
        return render(request, 'admin_templates/all_attendance', {'obj': st_obj, 'today': today, 'attendace_obj': res})
    else:
        obj = attendance.objects.filter(date=date).values("sd_id")
        res = [sub['sd_id'] for sub in obj]
        st_obj = student.objects.all()
        return render(request, 'admin_templates/all_attendance.html',
                      {'obj': st_obj, 'today': date, 'attendace_obj': res})

def add_fees(request):
    if request.method=="POST" and 'individual' in request.POST:
        month =date.today().strftime("%m")
        year =date.today().strftime("%Y")
        created_date = date.today().strftime("%Y-%m-%d")
        sd_id =request.POST['sd_id']
        status =0
        student_info=student.objects.get(sd_id=sd_id)
        mess_fee=request.POST['mess_fee']
        fine=request.POST['fine']
        accommodation=request.POST['accommodation']
        common=request.POST['common']
        total=request.POST['total']
        form =add_fee_ind(request.POST)
        print(form.errors)
        if form.is_valid():
            print("form is valid")
            obj= fees()
            obj.sd_id = sd_id
            obj.status = status
            obj.month = month
            obj.year = year
            obj.created_date = created_date
            obj.student_info = student_info
            obj.student_info_id = sd_id
            obj.mess_fee = mess_fee
            obj.fine = fine
            obj.accommodation = accommodation
            obj.common = common
            obj.total = total
            obj.save()
            print("saved")
            return redirect('all_fees_list')
        else:
            form =add_fee_ind()


    return render(request,'admin_templates/fees.html')


def all_fees(request):
    obj =fees.objects.all()
    return render(request,'admin_templates/all_fees.html',{'obj':obj})

def pending_fee(request):
    obj=fees.objects.filter(status=0).all()
    return render(request,'admin_templates/pending_fee.html',{'obj':obj})