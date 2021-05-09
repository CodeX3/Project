from datetime import date

from django.conf import settings
from django.shortcuts import render, redirect
from User.models import *
from Student.decorators import *
# Create your views here.
from Student.decorators import *


@studentonly
def load_index(request):
    id =request.session.get('userid')
    user = student.objects.get(sd_id=id)
    return render(request,'student_templates/index.html',{'user':user})
def logout(request):
    request.session.flush()
    return redirect('student_login')
@studentonly
def student_profile(request):
    id = request.session.get('userid')
    user = student.objects.get(sd_id=id)

    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        try:
            user.sd_name = request.POST['sd_name']
            user.sd_address = request.POST['sd_address']
            user.sd_email = request.POST['sd_email']
            user.sd_phone = request.POST['sd_phone']
            user.sd_university_register = request.POST['sd_university_register']
            user.sd_password = request.POST['sd_password']
            if len(request.FILES) != 0:
                user.sd_pic = request.FILES['sd_pic']
            user.save()
            return render(request, 'student_templates/profile.html',
                          {'user': user, 'media_url': settings.MEDIA_URL, 'success': True})
        except Exception as e:
            return render(request, 'student_templates/profile.html',
                          {'user': user, 'media_url': settings.MEDIA_URL, 'err': True})

    return render(request,'student_templates/profile.html',{'user':user,'media_url': settings.MEDIA_URL})

@studentonly
def student_parent_show(request):
    id = request.session.get('userid')
    user = student.objects.get(sd_id=id)

    return render(request,'student_templates/parent.html',{'user':user})

@studentonly
def table(request):
    id = request.session.get('userid')
    user = student.objects.get(sd_id=id)
    return render(request,'student_templates/table.html' ,{'user':user})
@studentonly
def students_view(request):
    id = request.session.get('userid')
    user = student.objects.get(sd_id=id)
    obj = student.objects.all()
    return render(request, 'student_templates/students_list.html',{'user':user,'obj':obj})

@studentonly
def student_today_attendance(request):
    id = request.session.get('userid')
    user = student.objects.get(sd_id=id)
    today = date.today().strftime("%Y-%m-%d")
    obj = attendance.objects.filter(date=today).values("sd_id")
    res = [sub['sd_id'] for sub in obj]
    st_obj = student.objects.all()
    print(res)
    if id in res:
        present =True
    else:
        present=False

    return render(request,'student_templates/today_attendance.html',{'user':user,'today':today,'attendace_obj': res,'obj':st_obj,'present':present})