import json
from django.shortcuts import render, redirect
from .models import *
from .forms import *

#---------------------------Login--------------------------------#
def do_login(request):
    if request.method=="GET":
        return render(request,'login.html')
    if request.method=="POST":
        print("post request recieved")
        response=redirect('/test')
        return response






#------------------------------USER ---------------------------------#
# 404 handler
def handler404(request, exception):
    return render(request, '404.html', locals())


def test(request):
    obj = register_new_user.objects.all()
    context = {'all_details': obj}
    return render(request, 'test.html', context)

def load_index(request):
    render(request, 'index.html')


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


#---------------------------Admin-------------------------------#

def load_admin_index(request):
    return render(request,'admin_templates/index.html')

def verify_students(request):
    obj=register_new_user.objects.all()
    context={'obj':obj}
    return render(request,'admin_templates/student_reg_verify.html',context)

def verify_students_confirm(request,pk):
    obj = register_new_user.objects.get(id=pk)
    print(obj)
    return render(request,'admin_templates/validate_student.html')

def table(request):
    return  render(request,'admin_templates/table.html')