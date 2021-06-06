from datetime import datetime
from django.urls import path, register_converter
from .import views
from  django.conf.urls import (handler404)
from  django.conf import settings
from django.conf.urls.static import static
class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value

register_converter(DateConverter, 'yyyy')


handler404='User.views.handler404'
urlpatterns = [
    path('register',views.do_register,name='register'),
    # path('',views.load_index),
    # path('test',views.test),
    # #
    # path('login',views.do_login,name='login'),
    path('',views.load_admin_index,name="dashboard"),
    path('verification',views.verify_students,name='verify_students'),
    path('table',views.table),
    # path('contact',views.load_contact),
    path('verification/<int:pk>',views.verify_students_confirm,name='confirm_student'),
    path('students',views.view_students,name='view_student_all'),
    path('students/edit/<int:pk>',views.edit_student,name='edit_student_details'),
    path('visitors',views.view_visitors,name='view_visitors'),
    path('complaints',views.view_complaints,name='admin_complaints'),
    # path('admin/review_complain',views.review_complaint),
    path('complaints',views.reg_complaint),
    path('today',views.today_attendance,name="today_attendance"),
    # path('admin/mark_attendance',views.mark_attendance),
    path('view/',views.general_attendance,name="common_attendance"),
    path('view/<yyyy:date>',views.date_attendance,name="attendance_date"),
    path('fees',views.add_fees,name="add_fees"),
    path('all_fees',views.all_fees,name="all_fees_list"),
    path('pending_fee',views.pending_fee,name="fee_pending"),
    path('service',views.service_list,name="service"),
    path('warden',views.show_warden,name='warden'),
    # path('admin',views.admin_login,name='admin_login'),
    path('logout',views.admin_logout,name='logout_admin'),
    path('scholarship',views.scholarship,name="scholarship"),
    path('scholarshipview',views.scholarshipview,name="scholarshipview"),
    path('live',views.livefe),
    path('security_live',views.livefe,name='security'),
    path('parent',views.parent_view,name='parent'),
    path('profile',views.admin_profile,name='admin_profile'),
    path('profile/<int:pk>',views.show_profile,name='show_profile'),
    # path('gen',views.generate_excel_all),
    path('download/',views.download_file),
    path('report',views.report,name='report'),
    path('test_mail',views.sent_mail_to_user),
    path('close_service',views.close_service,name='close_service'),






]
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)