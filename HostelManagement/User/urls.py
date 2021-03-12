from django.urls import path
from .import views
from  django.conf.urls import (handler404)

handler404='User.views.handler404'
urlpatterns = [
    path('register',views.do_register),
    path('',views.load_index),
    path('test',views.test),
    path('register/check',views.verify_reg,name="user_register" ),
    path('redirect',views.redirect_test),
]
