from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import redirect
from User.models import *
from .models import *
def studentonly(function):
    def wrap(request, *args, **kwargs):
        try:
            entry = student.objects.get(sd_id=request.session.get('userid'))
            print(entry)
            return function(request, *args, **kwargs)
        except ObjectDoesNotExist :
            print('not logged')
            return redirect('student_login')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap