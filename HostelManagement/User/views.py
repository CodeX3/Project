import calendar
import os
from datetime import date
from django.conf import settings
from django.core.exceptions import *
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from .decorators import *
from .forms import *
# live camera
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
from django.core.mail import send_mail
cam = None
import xlrd, xlsxwriter


# ---------------------------Login--------------------------------#
def do_login(request):
    value = request.session.get('userid')
    if value is not None:
        return redirect('student_home')
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            obj = student.objects.get(sd_email=email, sd_password=password)
        except ObjectDoesNotExist:
            return render(request, 'login.html', {'err': True})
        request.session['userid'] = obj.sd_id
        return redirect('student_home')


def admin_login(request):
    value = request.session.get('admin')
    if value is not None:
        return redirect('dashboard')
    if request.method == "GET":
        return render(request, 'admin_login.html')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)
        try:
            obj = warden.objects.get(email=email, password=password)
        except ObjectDoesNotExist:
            return render(request, 'admin_login.html', {'err': True})
        if obj.status:
            request.session['admin'] = obj.id
            return redirect('dashboard')
        else:

            return render(request, 'admin_login.html', {'active': True})

def parent_login(request):
    value = request.session.get('stdID')
    if value is not None:
        return redirect('parent_home')
    if request.method =='GET':
        return render(request, 'parent_login.html',)
    if request.method =="POST":
        stdPhone = request.POST['email']
        parentPhone = request.POST['password']
        try:
            obj = student.objects.get(sd_phone=stdPhone, sd_parent_phone=parentPhone)
        except ObjectDoesNotExist:
            return render(request,'parent_login.html',{'err':True})
        request.session['stdID'] = obj.sd_id
        return redirect('parent_home')

def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')


# ------------------------------USER ---------------------------------#
# 404 handler
def handler404(request, exception):
    return render(request, '404.html', locals())


def test(request):
    obj = register_new_user.objects.all()
    context = {'all_details': obj}
    return render(request, 'test.html', context)


def load_index(request):
    return render(request, 'index.html')


def do_register(request):
    if request.method == 'POST' and 'contact' in request.POST:
        form = contact_us(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            form = contact_us()
    if request.method == "POST" and 'submit' in request.POST:
        form = Register(request.POST)
        if form.is_valid():
            form.save()
            obj = {'status': True}
            return render(request, 'register_verification.html', obj)
        else:
            form = Register()
            obj = {'status': False}
            return render(request, 'register_verification.html', obj)
    return render(request, 'register.html')


# def load_contact(request):
#     if request.method =="POST" and 'contact' in request.POST:
#         print(request.body)
#         form =contact_us(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#         else:
#             form=contact_us()
#     obj = {'status': False}
#     return render(request,'register_verification.html',obj)


# ---------------------------Admin-------------------------------#

def get_notifications():
    noti = notification.objects.filter(status=1)
    val = noti.count()
    return noti,val
@adminonly
def load_admin_index(request):

    try:
        VideoCamera.__del__(cam)
    except Exception as e:
        print(e)
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    noti , val = get_notifications()
    return render(request, 'admin_templates/index.html', {'user': user,'notifications':noti,'notification_count':val})


@adminonly
def verify_students(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    obj = register_new_user.objects.all()
    noti, val = get_notifications()
    context = {'obj': obj, 'user': user,'notifications':noti,'notification_count':val}
    return render(request, 'admin_templates/student_reg_verify.html', context)


@adminonly
def verify_students_confirm(request, pk):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    obj = register_new_user.objects.get(id=pk)
    noti, val = get_notifications()
    context = {'obj': obj, 'user': user,'notifications':noti,'notification_count':val}

    if request.method == "POST":
        form = Student_add(request.POST)

        if form.is_valid():
            form.save()
            obj.delete()
            return redirect('/dashboard/verification', {'alert': True})
        else:
            form = Student_add()

    return render(request, 'admin_templates/validate_student.html', context)


@adminonly
def table(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    noti, val = get_notifications()
    return render(request, 'admin_templates/table.html', {'user': user,'notifications':noti,'notification_count':val})


@adminonly
def view_students(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    obj = student.objects.all()
    noti, val = get_notifications()
    context = {'obj': obj, 'user': user,'notifications':noti,'notification_count':val}
    return render(request, 'admin_templates/student_view.html', context)


@adminonly
def edit_student(request, pk):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    obj = student.objects.get(sd_id=pk)
    noti, val = get_notifications()
    context = {'obj': obj, 'user': user,'notifications':noti,'notification_count':val}

    if request.method == "POST":
        form = Student_edit(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/students')
        else:
            print("not valid")
    return render(request, 'admin_templates/edit_student.html', context)


@adminonly
def view_visitors(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    obj = visitor.objects.all()
    noti, val = get_notifications()
    return render(request, 'admin_templates/visitor.html', {'obj': obj, 'user': user,'notifications':noti,'notification_count':val})


@adminonly
def view_complaints(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    obj = complaint.objects.all()
    noti, val = get_notifications()
    return render(request, 'admin_templates/complaint.html', {'obj': obj, 'user': user,'notifications':noti,'notification_count':val})


@adminonly
def review_complaint(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    obj = complaint.objects.get(id=request.GET['id'])
    obj.status = "closed"
    obj.save()
    return HttpResponse(status=200)


@adminonly
def reg_complaint(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    noti, val = get_notifications()
    if request.method == "POST":
        form = complaints(request.POST)
        if form.is_valid():
            form.save()
        else:
            form = complaints()
    return render(request, 'complaint_insert.html', {'user': user,'notifications':noti,'notification_count':val})


@adminonly
def today_attendance(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    today = date.today()
    obj = attendance.objects.filter(date=today).values("sd_id")
    res = [sub['sd_id'] for sub in obj]
    st_obj = student.objects.all()
    noti, val = get_notifications()
    return render(request, 'admin_templates/today_attendance.html',
                  {'obj': st_obj, 'today': today, 'attendace_obj': res, 'user': user,'notifications':noti,'notification_count':val})


@adminonly
def mark_attendance(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    try:
        today = date.today().strftime("%Y-%m-%d")
        obj = attendance.objects.get(sd_id=request.GET['id'], date=today)
    except ObjectDoesNotExist:
        print(date.today().strftime("%Y-%m-%d"))
        obj = attendance()
        student_data = student.objects.get(sd_id=request.GET['id'])
        obj.status = 1
        obj.sd_id = request.GET['id']
        obj.date = date.today().strftime("%Y-%m-%d")
        obj.stduent_info = student_data
        obj.month = int(date.today().strftime("%m"))
        obj.year = int(date.today().strftime("%Y"))
        obj.sd_name = student_data.sd_name
        obj.save()

    return HttpResponse(status=200)


@adminonly
def general_attendance(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    lev = leave.objects.all()
    noti, val = get_notifications()
    return render(request, 'admin_templates/category_view.html', {'user': user, 'obj': lev,'notifications':noti,'notification_count':val})


@adminonly
def date_attendance(request, date=None):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    noti, val = get_notifications()
    if date is None:
        today = date.today().strftime("%Y-%m-%d")
        obj = attendance.objects.filter(date=today).values("sd_id")
        res = [sub['sd_id'] for sub in obj]
        st_obj = student.objects.all()
        return render(request, 'admin_templates/all_attendance',
                      {'obj': st_obj, 'today': today, 'attendace_obj': res, 'user': user,'notifications':noti,'notification_count':val})
    else:
        obj = attendance.objects.filter(date=date).values("sd_id")
        res = [sub['sd_id'] for sub in obj]
        st_obj = student.objects.all()
        return render(request, 'admin_templates/all_attendance.html',
                      {'obj': st_obj, 'today': date, 'attendace_obj': res, 'user': user,'notifications':noti,'notification_count':val})


@adminonly
def add_fees(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    noti, val = get_notifications()
    if request.method == "POST" and 'individual' in request.POST:
        month = date.today().strftime("%m")
        year = date.today().strftime("%Y")
        created_date = date.today().strftime("%Y-%m-%d")
        sd_id = request.POST['sd_id']
        status = 0
        student_info = student.objects.get(sd_id=sd_id)
        mess_fee = request.POST['mess_fee']
        fine = request.POST['fine']
        accommodation = request.POST['accommodation']
        common = request.POST['common']
        total = request.POST['total']
        form = add_fee_ind(request.POST)
        # print(form.errors)
        if form.is_valid():
            obj = fees()
            obj.sd_id = sd_id
            obj.status = status
            obj.month = month
            obj.year = year
            obj.created_date = created_date
            obj.student_info = student_info
            obj.student_info_id = sd_id
            obj.mess_fee = mess_fee
            obj.fine = fine
            obj.accommodation = accommodation
            obj.common = common
            obj.total = total
            obj.save()
            # print("saved")
            return redirect('all_fees_list')
        else:
            form = add_fee_ind()
    if request.method == "POST" and 'all' in request.POST:
        all_student = student.objects.all()
        month = int(date.today().strftime("%m"))
        year = int(date.today().strftime("%Y"))

        for i in all_student:
            present = attendance.objects.filter(sd_id=i.sd_id, month=month, year=year).count()
            mess_fee = int(request.POST['mess_fee'])
            mess_fee = mess_fee * present
            # print(i.sd_id,present,":",mess_fee)
            accommodation = request.POST['accommodation']
            common = request.POST['common']
            total = int(request.POST['total'])
            total = total + mess_fee
            # print(total)
            obj = fees()
            obj.sd_id = i.sd_id
            obj.status = 0
            obj.month = month
            obj.year = year
            obj.created_date = date.today().strftime("%Y-%m-%d")
            obj.student_info = i
            obj.student_info_id = i.sd_id
            obj.mess_fee = mess_fee
            obj.accommodation = accommodation
            obj.common = common
            obj.total = total
            obj.save()
        return redirect('all_fees_list')

    return render(request, 'admin_templates/fees.html', {'user': user,'notifications':noti,'notification_count':val})


@adminonly
def all_fees(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    obj = fees.objects.all()
    user = warden.objects.get(id=value)
    noti, val = get_notifications()
    return render(request, 'admin_templates/all_fees.html', {'obj': obj, 'user': user,'notifications':noti,'notification_count':val})


@adminonly
def pending_fee(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    obj = fees.objects.filter(status=0).all()
    noti, val = get_notifications()
    return render(request, 'admin_templates/pending_fee.html', {'obj': obj, 'user': user,'notifications':noti,'notification_count':val})

@adminonly
def parent_all_fee(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    obj = fees.objects.all()
    user = warden.objects.get(id=value)
    return render(request, 'admin_templates/parent_all_fee.html', {'user': user, 'obj': obj})

@adminonly
def service_list(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    open_service = service.objects.filter(status='open')
    closed_service = service.objects.filter(status='closed')
    noti, val = get_notifications()
    return render(request, 'admin_templates/service.html', {'user': user,'open':open_service,'closed':closed_service,'notifications':noti,'notification_count':val})


@adminonly
def show_warden(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    admin_id = request.session.get('admin')
    all_warden = warden.objects.all()
    check_super_admin = warden.objects.get(id=admin_id)
    check_super_admin = check_super_admin.is_main
    noti, val = get_notifications()
    if request.method == "POST":
        try:
            obj = warden()
            obj.name = request.POST['name']
            obj.address = request.POST['address']
            obj.password = request.POST['password']
            obj.email = request.POST['email']
            obj.incharge = request.POST['incharge']
            obj.phone = request.POST['phone']
            print(request.POST)
            if 'status' in request.POST:
                obj.status = True
            else:
                obj.status = False
            obj.save()
            return render(request, 'admin_templates/warden.html',
                          {'obj': all_warden, 'media_url': settings.MEDIA_URL, 'edit': check_super_admin, 'reg': True,
                           'user': user,'notifications':noti,'notification_count':val})
        except Exception as e:
            print(e)
            return render(request, 'admin_templates/warden.html',
                          {'obj': all_warden, 'media_url': settings.MEDIA_URL, 'edit': check_super_admin, 'reg': False,
                           'user': user,'notifications':noti,'notification_count':val})
    return render(request, 'admin_templates/warden.html',
                  {'obj': all_warden, 'media_url': settings.MEDIA_URL, 'edit': check_super_admin, 'reg': True,
                   'user': user,'notifications':noti,'notification_count':val})

@adminonly
def scholarshipview(request):
    value = request.session.get('admin')
    user = warden.objects.get(id=value)
    selected = marks.objects.order_by('-total')
    selected = marks.objects.first()
    print(selected)
    return render(request, 'admin_templates/scholarshipview.html', {'obj': selected,'user':user})


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        # capture = cv2.VideoCapture('rtsp://username:password@192.168.1.64/1')
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livefe(request):
    try:
        global cam
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        print("cam error")
        pass


@adminonly
def parent_view(request):
    noti, val = get_notifications()
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    parent = student.objects.all()
    return render(request, 'admin_templates/parent.html', {'user': user, 'obj': parent,'notifications':noti,'notification_count':val})


@adminonly
def admin_profile(request):
    value = request.session.get('admin')
    user = warden.objects.get(id=value)
    noti, val = get_notifications()
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        try:
            user.name = request.POST['name']
            user.address = request.POST['address']
            user.email = request.POST['email']
            user.phone = request.POST['phone']
            user.incharge = request.POST['incharge']
            user.password = request.POST['password']
            if len(request.FILES) != 0:
                user.pic = request.FILES['pic']
            user.save()
            return render(request, 'admin_templates/profile.html',
                          {'user': user, 'media_url': settings.MEDIA_URL, 'success': True,'notifications':noti,'notification_count':val})
        except Exception as e:
            return render(request, 'admin_templates/profile.html',
                          {'user': user, 'media_url': settings.MEDIA_URL, 'err': True,'notifications':noti,'notification_count':val})
    return render(request, 'admin_templates/profile.html', {'user': user, 'media_url': settings.MEDIA_URL,'notifications':noti,'notification_count':val})


@adminonly
def show_profile(request, pk):
    value = request.session.get('admin')
    noti, val = get_notifications()
    if pk == value:
        return redirect('admin_profile')
    user = warden.objects.get(id=value)
    try:
        obj = warden.objects.get(id=pk)
    except ObjectDoesNotExist:
        return redirect('warden')
    if request.method == "POST":
        try:
            obj.name = request.POST['name']
            obj.address = request.POST['address']
            obj.email = request.POST['email']
            obj.phone = request.POST['phone']
            obj.incharge = request.POST['incharge']
            obj.password = request.POST['password']
            if len(request.FILES) != 0:
                obj.pic = request.FILES['pic']
            if 'status' in request.POST:
                obj.status = True
            else:
                obj.status = False
            print(obj)
            obj.save()
            return render(request, 'admin_templates/show_profile.html',
                          {'user': user, 'media_url': settings.MEDIA_URL, 'success': True, 'obj': obj,'notifications':noti,'notification_count':val})
        except Exception as e:
            return render(request, 'admin_templates/show_profile.html',
                          {'user': user, 'media_url': settings.MEDIA_URL, 'err': True, 'obj': obj,'notifications':noti,'notification_count':val})
    return render(request, 'admin_templates/show_profile.html',
                  {'user': user, 'media_url': settings.MEDIA_URL, 'obj': obj,'notifications':noti,'notification_count':val})


@adminonly
def alter_warden(request):
    try:
        obj = warden.objects.get(id=request.GET['id'])
        if obj.status:
            obj.status = False
        else:
            obj.status = True
        obj.save()
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=400)


@adminonly
def delete_warden(request):
    try:
        obj = warden.objects.get(id=request.GET['id'])
        obj.delete()
        return HttpResponse(status=200)
    except Exception:
        return HttpResponse(status=400)


def addDataToSheet(worksheet):
    # first row
    worksheet.write(1, 0, "2001")
    worksheet.write(1, 1, "James")
    worksheet.write(1, 2, "Computer")
    worksheet.write(1, 3, "A")
    # Second row
    worksheet.write(2, 0, "2002")
    worksheet.write(2, 1, "Jhones")
    worksheet.write(2, 2, "Electronics")
    worksheet.write(2, 3, "A+")
    # Third row
    worksheet.write(3, 0, "2003")
    worksheet.write(3, 1, "Micheal")
    worksheet.write(3, 2, "Civil")
    worksheet.write(3, 3, "C")


def generate_excel(id, y, m):
    rootPath = os.getcwd() + "\\" + "report\\"
    print(rootPath)
    import datetime
    # file = (rootPath+"test.xlsx")
    file = (rootPath + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".xlsx")
    # file path
    print(file)
    workbook = xlsxwriter.Workbook(file)

    # The workbook object is then used to add new
    # worksheet via the add_worksheet() method.
    worksheet = workbook.add_worksheet()
    cell_formate_present = workbook.add_format()
    cell_formate_present.set_bg_color('#00FF00')
    cell_formate_absent = workbook.add_format()
    cell_formate_absent.set_font_color('red')
    row = 1
    col = 0
    worksheet.write(0, 0, "Date")
    worksheet.write(0, 1, "Attendance")

    obj = attendance.objects.filter(sd_id=id, month=m, year=y).values("date")
    start = datetime.date(year=y, month=m, day=1)
    today = datetime.date.today()
    endDay = calendar.monthrange(y, m)[1]
    end = datetime.date(year=y, month=m, day=endDay)
    if today >= end:
        print("true or same")
    else:
        end = today
    res = [sub['date'].strftime("%Y-%m-%d") for sub in obj]
    count = (end - start).days
    loopVar = start
    while count >= 0:
        worksheet.write(row, col, loopVar.strftime("%Y-%m-%d"))
        if loopVar.strftime("%Y-%m-%d") in res:
            worksheet.write(row, col + 1, "Present", cell_formate_present)
        else:
            worksheet.write(row, col + 1, "Absent", cell_formate_absent)
        loopVar += datetime.timedelta(days=1)
        row += 1
        count -= 1
    workbook.close()

    return file


def generate_excel_all(y, m):
    rootPath = os.getcwd() + "\\" + "report\\"
    print(rootPath)
    import datetime
    # file = (rootPath+"test.xlsx")
    file = (rootPath + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".xlsx")
    # file path
    print(file)
    workbook = xlsxwriter.Workbook(file)

    # The workbook object is then used to add new
    # worksheet via the add_worksheet() method.
    worksheet = workbook.add_worksheet()
    cell_formate_present = workbook.add_format()
    cell_formate_present.set_bg_color('#00FF00')
    cell_formate_absent = workbook.add_format()
    cell_formate_absent.set_font_color('red')

    start = datetime.date(year=y, month=m, day=1)
    today = datetime.date.today()
    endDay = calendar.monthrange(y, m)[1]
    end = datetime.date(year=y, month=m, day=endDay)
    if today >= end:
        print("true or same")
    else:
        end = today

    count = (end - start).days

    row = 1
    col = 0
    worksheet.write(0, 0, "Name")
    i = 1
    loopVar = start
    print(count, loopVar)
    while count >= 0:
        worksheet.write(0, i, loopVar.strftime("%Y-%m-%d"))
        loopVar += datetime.timedelta(days=1)
        i += 1
        count -= 1

    student_id = student.objects.all().values('sd_id')
    for i in student_id:
        obj = attendance.objects.filter(sd_id=i['sd_id'], month=m, year=y).values("date")
        res = [sub['date'].strftime("%Y-%m-%d") for sub in obj]
        loopVar = start
        name = student.objects.get(sd_id=i['sd_id'])

        worksheet.write(row, col, name.sd_name)
        col += 1
        count = (end - start).days
        while count >= 0:
            if loopVar.strftime("%Y-%m-%d") in res:
                worksheet.write(row, col, "Present", cell_formate_present)
            else:
                worksheet.write(row, col, "Absent", cell_formate_absent)
            loopVar += datetime.timedelta(days=1)
            col += 1
            count -= 1
        row += 1
        col = 0
    workbook.close()
    return file


def download_file_all(request, y, m):
    path = generate_excel_all(y, m)
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def download_file(request, id, y, m):
    path = generate_excel(id, y, m)
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


@adminonly
def report(request):
    noti, val = get_notifications()
    value = request.session.get('admin')
    user = warden.objects.get(id=value)
    flag = False
    if request.method == "POST":
        print(request.POST)
        if request.POST['id'] == "":
            flag = True
        id = request.POST['id']
        data = request.POST['month']
        y, m = data.split("-", 2)
        if flag:
            response = download_file_all(request, int(y), int(m))
        else:
            response = download_file(request, int(id), int(y), int(m))
        return response
    return render(request, 'admin_templates/report.html', {'user': user,'notifications':noti,'notification_count':val})

def sent_mail_to_user(request):
    send_mail('','','',[''],fail_silently=False)
    return HttpResponse(status=200)

@adminonly
def close_service(request):
    val = request.GET['id']
    try:
        obj = service.objects.get(id=val)
        obj.status='closed'
        obj.closed=date.today().strftime("%Y-%m-%d")
        obj.save()
        return HttpResponse(status=200)
    except Exception as e:
        print(e)
        return HttpResponse(status=500)
@adminonly
def Menu(request):
    noti, val = get_notifications()
    value = request.session.get('admin')
    user = warden.objects.get(id=value)
    obj = mess_menu.objects.all()

    return render (request,'admin_templates/Menu.html',{'notifications':noti,'notification_count':val,'user':user,'obj':obj})

def update_menu(request):


    try:
        obj = mess_menu.objects.get(day=request.GET['day'])
        obj.mng = request.GET['mng']
        obj.noon = request.GET['noon']
        obj.night = request.GET['night']
        obj.save()
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=500)

