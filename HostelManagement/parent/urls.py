from datetime import datetime

from django.conf import settings
from django.urls import path, register_converter
from .import views
from  django.conf.urls import (handler404)
from django.conf.urls.static import static



urlpatterns = [
    path('',views.load_index,name='parent_home'),
    path('profile',views.load_student_profile,name="parent_student_profile")

]
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)