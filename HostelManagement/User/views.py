from datetime import date
from django.conf import settings
from django.core.exceptions import *
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .decorators import *
from .forms import *
# live camera
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
cam = None
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
    return render(request, 'admin_templates/index.html', {'user': user})

@adminonly
def verify_students(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    obj = register_new_user.objects.all()
    context = {'obj': obj, 'user': user}
    return render(request, 'admin_templates/student_reg_verify.html', context)

@adminonly
def verify_students_confirm(request, pk):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    obj = register_new_user.objects.get(id=pk)
    context = {'obj': obj, 'user': user}

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
    return render(request, 'admin_templates/table.html', {'user': user})

@adminonly
def view_students(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    obj = student.objects.all()
    context = {'obj': obj, 'user': user}
    return render(request, 'admin_templates/student_view.html', context)

@adminonly
def edit_student(request, pk):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    obj = student.objects.get(sd_id=pk)
    context = {'obj': obj, 'user': user}

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

    return render(request, 'admin_templates/visitor.html', {'obj': obj, 'user': user})

@adminonly
def view_complaints(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    obj = complaint.objects.all()

    return render(request, 'admin_templates/complaint.html', {'obj': obj, 'user': user})

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
    if request.method == "POST":
        form = complaints(request.POST)
        if form.is_valid():
            form.save()
        else:
            form = complaints()
    return render(request, 'complaint_insert.html', {'user': user})

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
    return render(request, 'admin_templates/today_attendance.html',
                  {'obj': st_obj, 'today': today, 'attendace_obj': res, 'user': user})

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
    return render(request, 'admin_templates/category_view.html', {'user': user})

@adminonly
def date_attendance(request, date=None):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    if date is None:
        today = date.today().strftime("%Y-%m-%d")
        obj = attendance.objects.filter(date=today).values("sd_id")
        res = [sub['sd_id'] for sub in obj]
        st_obj = student.objects.all()
        return render(request, 'admin_templates/all_attendance',
                      {'obj': st_obj, 'today': today, 'attendace_obj': res, 'user': user})
    else:
        obj = attendance.objects.filter(date=date).values("sd_id")
        res = [sub['sd_id'] for sub in obj]
        st_obj = student.objects.all()
        return render(request, 'admin_templates/all_attendance.html',
                      {'obj': st_obj, 'today': date, 'attendace_obj': res, 'user': user})

@adminonly
def add_fees(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
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

    return render(request, 'admin_templates/fees.html', {'user': user})

@adminonly
def all_fees(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    obj = fees.objects.all()
    user = warden.objects.get(id=value)
    return render(request, 'admin_templates/all_fees.html', {'obj': obj, 'user': user})

@adminonly
def pending_fee(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    obj = fees.objects.filter(status=0).all()
    return render(request, 'admin_templates/pending_fee.html', {'obj': obj, 'user': user})

@adminonly
def service_list(request):
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    return render(request, 'admin_templates/service.html', {'user': user})

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
                           'user': user})
        except Exception as e:
            print(e)
            return render(request, 'admin_templates/warden.html',
                          {'obj': all_warden, 'media_url': settings.MEDIA_URL, 'edit': check_super_admin, 'reg': False,
                           'user': user})
    return render(request, 'admin_templates/warden.html',
                  {'obj': all_warden, 'media_url': settings.MEDIA_URL, 'edit': check_super_admin, 'reg': True,
                   'user': user})

@adminonly
def scholarship(request):
    if request.method == 'POST':
        print(request.POST)
        num = request.POST['sd_admno']
        try:
            st = student.objects.get(sd_admno=num)

        except ObjectDoesNotExist:
            return render(request, 'admin_templates/scholarship.html', {'err': True})
        obj = marks()
        obj.sd_id = int(st.sd_id)
        obj.sd_name = st.sd_name
        obj.sd_admno = st.sd_admno
        obj.mark1 = int(request.POST['mark1'])
        obj.mark2 = int(request.POST['mark2'])
        obj.total = int(request.POST['total'])
        obj.save()
        print("saved")
    return render(request, 'admin_templates/scholarship.html')

@adminonly
def scholarshipview(request):
    selected = marks.objects.order_by('-total')
    selected = marks.objects.first()
    print(selected)
    return render(request, 'admin_templates/scholarshipview.html', {'obj': selected})


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
    value = request.session.get('admin')
    # if value is None:
    #     return redirect('admin_login')
    user = warden.objects.get(id=value)
    parent = student.objects.all()
    return render(request,'admin_templates/parent.html',{'user':user,'obj':parent})

@adminonly
def admin_profile(request):
    value = request.session.get('admin')
    user = warden.objects.get(id=value)
    if request.method=="POST":
        print(request.POST)
        print(request.FILES)
        try:
            user.name = request.POST['name']
            user.address = request.POST['address']
            user.email = request.POST['email']
            user.phone = request.POST['phone']
            user.incharge = request.POST['incharge']
            user.password = request.POST['password']
            if len(request.FILES) !=0:
                user.pic = request.FILES['pic']
            user.save()
            return render(request, 'admin_templates/profile.html', {'user': user, 'media_url': settings.MEDIA_URL,'success':True})
        except Exception as e:
            return render(request, 'admin_templates/profile.html', {'user': user, 'media_url': settings.MEDIA_URL,'err':True })
    return render(request,'admin_templates/profile.html',{'user':user,'media_url': settings.MEDIA_URL})

@adminonly
def show_profile(request,pk):
    value = request.session.get('admin')
    if pk ==value:
        return redirect('admin_profile')
    user = warden.objects.get(id=value)
    try:
        obj =warden.objects.get(id=pk)
    except ObjectDoesNotExist:
        return redirect('warden')
    return render(request,'admin_templates/show_profile.html',{'user':user,'media_url': settings.MEDIA_URL,'obj':obj})