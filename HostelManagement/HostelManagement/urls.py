"""HostelManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from User import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin_templates/', admin.site.urls),
    path('dashboard/',include('User.urls')),
    path('image/',include('image.urls')),
    path('homepage/',include('Student.urls')),
    path('guest/',include('guest.urls')),
    path('',views.load_index,name="FrontPage"),
    path('login', views.do_login, name='student_login'),
    path('register', views.do_register, name='register'),
    path('admin',views.admin_login,name='admin_login'),
    path('admin/alter_warden', views.alter_warden),
    path('admin/mark_attendance',views.mark_attendance),
    path('admin/review_complain',views.review_complaint),
    path('admin/delete_warden',views.delete_warden),
    path('parent/',include('parent.urls')),
    path('parent_login',views.parent_login,name='parent_login'),
    path('admin/alter_menu',views.update_menu),
    path('admin/update_food',views.update_food),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)