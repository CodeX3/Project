from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import redirect
from User.models import *
from .models import *
def parentOnly(function):
    def wrap(request, *args, **kwargs):
        try:
            entry = student.objects.get(sd_id=request.session.get('stdID'))
            print(entry)
            return function(request, *args, **kwargs)
        except ObjectDoesNotExist :
            print('not logged')
            return redirect('parent_login')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap