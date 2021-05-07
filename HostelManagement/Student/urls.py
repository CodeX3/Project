from datetime import datetime

from django.conf import settings
from django.urls import path, register_converter
from .import views
from  django.conf.urls import (handler404)
from django.conf.urls.static import static



urlpatterns = [
   path('',views.load_index,name='student_home'),
   path('logout',views.logout,name='logout'),
   path('profile',views.student_profile,name='student_profile'),
   path('parent',views.student_parent_show,name='student_parent_show'),
   path('table',views.table,name='student_table'),

]
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)