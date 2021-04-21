from django.urls import path
from .import views
from  django.conf.urls import (handler404)

handler404='User.views.handler404'
urlpatterns = [
    path('register',views.do_register),
    path('',views.load_index),
    path('test',views.test),
    #
    path('login',views.do_login),
    path('dashboard',views.load_admin_index,name="dashboard"),
    path('dashboard/verification',views.verify_students,name='verify_students'),
    path('table',views.table),
    # path('contact',views.load_contact),
    path('dashboard/verification/<int:pk>',views.verify_students_confirm,name='confirm_student'),
    path('dashboard/students',views.view_students,name='view_student_all'),
    path('dashboard/students/edit/<int:pk>',views.edit_student,name='edit_student_details'),
    path('dashboard/visitors',views.view_visitors,name='view_visitors'),
    path('dashboard/complaints',views.view_complaints,name='admin_complaints'),
    path('admin/review_complain',views.review_complaint),
    path('complaints',views.reg_complaint),
    path('dashboard/today',views.today_attendance,name="today_attendance"),
    path('admin/mark_attendance',views.mark_attendance),

]
