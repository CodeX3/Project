from datetime import datetime

from django.conf import settings
from django.urls import path, register_converter
from .import views
from  django.conf.urls import (handler404)
from django.conf.urls.static import static



urlpatterns = [
    path('',views.load_index,name='parent_home'),
    path('profile',views.load_student_profile,name="parent_student_profile"),
    path('add-visitor',views.add_visitor,name='parent_add_visitor'),
    path('contact',views.contact,name='contact'),
    path('visitor',views.visitor_view,name='parent_visitor'),
    path('fee',views.payment_view,name='parent_fee'),
    path('logout',views.logout,name="parent_logout"),
    path('list-parents',views.list_parents,name='parent_list'),
    path('complaints',views.complaints,name="parent_complaints"),
    path('add_complaints',views.add_complaint,name="parent_add_complaints"),
]
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)