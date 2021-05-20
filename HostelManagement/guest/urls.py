from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import  static


urlpatterns = [
    path('guestregister', views.guestreg,name="guest registration"),
    path('allguest', views.allguest,name="all guest"),
    path('',views.guest_present,name="guest present"),

]