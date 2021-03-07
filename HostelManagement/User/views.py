from django.shortcuts import render

# Create your views here.
def load_index(request):
    render(request,'index.html')

def do_register(request):
    if request.method =="POST":
        print("request reviced")
    return render(request,'register.html')