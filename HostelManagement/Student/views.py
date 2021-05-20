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