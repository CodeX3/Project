from django.urls import path
from .import views

urlpatterns = [
    path('register',views.do_register ),
    path('',views.load_index),
]
