from django.shortcuts import render
from datetime import date


# Create your views here.
from .form import GuestRegister
from .models import register_guest
today=date.today()

def guestreg(request):

    if request.method == "POST":
        print(request.POST)
        form = GuestRegister(request.POST)
        if form.is_valid():
            obj=register_guest()
            print("Success")

            form.save()
        else:
            print('failed')
            print(form.errors)
            form = GuestRegister()
    return render(request,'guestreg.html',)

def allguest(request):
    obj = register_guest.objects.all()
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    #user = warden.objects.get(id=value)
    obj = register_guest.objects.all()
    context = {'obj': obj}
    return render(request, 'allguest.html', {'obj': obj})

def guest_present(request):
    today = date.today()
    res = register_guest.objects.all()
    for i in res:
        if i.ldate <= today:
            print("modified")
            i.status=False
            i.save()
        else:
            print(today,i.ldate)
    obj = register_guest.objects.all()
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    #user = warden.objects.get(id=value)
    obj=register_guest.objects.filter(status=1)
    context = {'obj': obj}
    return render(request, 'allguest.html', {'obj': obj})