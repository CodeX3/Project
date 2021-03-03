from django.shortcuts import render

# Create your views here.
def load_index(request):
    render(request,'index.html')

def do_register(request):
    return render(request,'register.html')