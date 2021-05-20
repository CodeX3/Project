from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import redirect

from .models import *
def adminonly(function):
    def wrap(request, *args, **kwargs):
        # entry = warden.objects.get(id=request.session.get('admin'))
        try:
            entry = warden.objects.get(id=request.session.get('admin'))
            print(entry)
            return function(request, *args, **kwargs)
        except ObjectDoesNotExist :
            print('not logged')
            return redirect('admin_login')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap