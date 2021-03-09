import json
from django.shortcuts import render
from .models import *
from .forms import *

#404 handler
def handler404(request,exception):
    return render(request,'404.html',locals())

def test(request):
    obj=register_new_user.objects.all()
    context = {'all_details': obj}
    return render(request, 'test.html', context)


def load_index(request):
    render(request,'index.html')


def do_register(request):
    if request.method =="POST":
        form =Register(request.POST)
        if form.is_valid():
            form.save()
        else:
            form =Register()
    return render(request,'register.html')