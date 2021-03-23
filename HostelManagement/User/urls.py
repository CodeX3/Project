from django.urls import path
from .import views
from  django.conf.urls import (handler404)

handler404='User.views.handler404'
urlpatterns = [
    path('register',views.do_register),
    # path('',views.load_index),
    path('test',views.test),
    #
    path('login',views.do_login),
    path('dashboard',views.load_admin_index,name="dashboard"),
    path('dashboard/verification',views.verify_students,name='verify_students'),
    path('table',views.table),
    # path('contact',views.load_contact),
    path('dashboard/verification/<int:pk>',views.verify_students_confirm,name='confirm_student'),
]
