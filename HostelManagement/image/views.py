from django.shortcuts import render

# Create your views here.
from .form import ImageForm
from .models import Image
from User.models import warden
def index(request):
    value = request.session.get('admin')
    user = warden.objects.get(id=value)
    if request.method == "POST":
        print("post method")
        form=ImageForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            obj=form.instance
            print("data stored")
            return render(request,"gallery.html",{"obj":obj,'user':user})
        else:
            print("rejected")
            form=ImageForm()

    form=ImageForm()
    img=Image.objects.all()
    print(img)
    return render(request,"gallery.html",{"img":img,"form":form,'user':user})

