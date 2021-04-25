from django.shortcuts import render

# Create your views here.
from .form import ImageForm
from .models import Image

def index(request):
    if request.method == "POST":
        print("post method")
        form=ImageForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            obj=form.instance
            print("data stored")
            return render(request,"gallery.html",{"obj":obj})
        else:
            print("rejected")
            form=ImageForm()

    form=ImageForm()
    img=Image.objects.all()
    print(img)
    return render(request,"gallery.html",{"img":img,"form":form})

