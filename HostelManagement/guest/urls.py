from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import  static


urlpatterns = [
    path('guestreg', views.guestreg,name="guest registration"),

]