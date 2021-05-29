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
   path('students_list', views.students_view, name='allstudents'),
   path('today',views.student_today_attendance,name='student_today'),
   path('pending_fee',views.student_pending_fee,name='student_pending_fee'),
   path('orders',views.test),
   path('callback',views.callback,name='callback'),
   path('all_fee',views.all_fee,name='student_all_fee'),
   path('complaints',views.complaints,name='student_complaints'),
   path('add_complaints',views.add_complaints,name='student_add_complaints'),
   path('leave',views.apply_leave,name='student_leave'),
   path('list-leave',views.list_leave,name='student_list_leave'),
   path('guests',views.guest,name='student_guest'),
   path('service',views.request_service,name='student_service'),
   path('service-requested',views.list_service_requested,name='student_list_service'),
   path('calender',views.show_calender),
   path('transactions',views.transaction_history,name="transactions"),
   path('visitor',views.visitor_view,name='student_visitor'),
   path('add-visitor',views.visitor_add,name='student_visitor_add'),
   path('monthly-attendance',views.report,name='student_report'),

]
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)