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
    return render(request,'student_templates/profile.html',{'user':user,'media_url': settings.MEDIA_URL})