from datetime import datetime
from django.urls import path, register_converter
from .import views
from  django.conf.urls import (handler404)




urlpatterns = [
   path('',views.load_index,name='student_home'),
   path('logout',views.logout,name='logout'),


]