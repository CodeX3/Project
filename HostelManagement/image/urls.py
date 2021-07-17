from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import  static


urlpatterns = [
    path('admin_image', views.admin_gallery,name="admin_gallery"),
    path('student_image', views.student_gallery,name="student_gallery"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)