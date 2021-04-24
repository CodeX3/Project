from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import  static


urlpatterns = [
    path('image', views.index,name="gallery"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)