from django.shortcuts import render, redirect
from User.models import *
# Create your views here.


def load_index(request):
    id =request.session.get('userid')
    if id is None:
        return  redirect('login')
    obj = student.objects.get(sd_id=id)
    return render(request,'student_templates/index.html',{'obj':obj})
def logout(request):
    request.session.flush()
    return redirect('login')