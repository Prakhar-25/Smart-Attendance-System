from django.shortcuts import render, redirect
from .models import Register,Attendance
from .recognition import train_image,recognize
from django.contrib import messages
from django.contrib.auth import  login, logout
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from datetime import datetime,date

# Create your views here.

def index(request):

    if request.method == 'POST':
        enrollment = request.POST['enrollment']
        password = request.POST['password']

        if not enrollment:
            messages.error(request,"Enrollment number is required.")
            return render(request,'index.html')
        if not password:
            messages.error(request,"Password is required.")
            return render(request,'index.html')
        try:
            user = Register.objects.get(enrollment = enrollment)
            if check_password(password,user.password):
                # login(request,user)
                request.session['user_id'] = user.id
                messages.success(request, "Login Successful")
                return redirect('login_view')
            else:
                messages.error(request,'Invalid Password')
        except Register.DoesNotExist:   
            messages.error(request,'Invalid enrollment no.')
        
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def login_view(request):
    return render(request,'logged_in.html')

def logout_view(request):
    logout(request)
    request.session['logged_out'] = True
    return redirect('index')

def register(request):

    if request.method == 'POST':
        enrollment = request.POST['enrollment']
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']
        branch = request.POST['branch']
        img = request.FILES.get('image')

        if Register.objects.filter(enrollment = enrollment).exists():
            messages.error(request,"Enrollment no. already exists.")
            return render(request, 'register.html')
        
        new_user = Register(enrollment = enrollment, name = name, email = email, mobile = mobile, branch = branch, password = password, img = img)
        new_user.save_user()
        train_image(img,name)
        messages.success(request, 'Registration successful! Please login.')
        return redirect('index')
    else :
        return render(request, 'register.html')
    
def attendance(request):
    if request.method == 'GET':
        student_name, camera_error = recognize()
        if camera_error:
            return JsonResponse({'error': 'Could not open video device'},status = 500)
        else:
            if student_name == "Unknown":
                return JsonResponse({'error': 'Student not registered. Kindly register'},status = 500)
            else:
                student = Register.objects.get(name = student_name)
                today_date = date.today()
                
                attendance,created = Attendance.objects.get_or_create(student = student, date = today_date)
                attendance.is_present = True
                attendance.save()
                messages.success(request, "Attendance has been marked successfully.")
                return redirect('login_view')
    
            
    return render(request,'logged_in.html')


# def faculty(request):
#     context = {
#         "total" : 50,
#         "present" : 36,
#         "absent": 14,
#         "percent": 72
#     }
#     return render(request, 'dashboard.html',context)

def dashboard(request):

    students = Register.objects.all()
    total = students.count()
    if request.method == 'POST':
        date = datetime.strptime(request.POST['date'],'%Y-%m-%d')
        attendees = Attendance.objects.filter(date = date)
        present = len(attendees)

        students_present = [attendee.student.enrollment for attendee in attendees]
        print("students_present:", students_present)
        context = {
            "total" : total,
            "present" : present,
            "absent": total - present,
            "percent": round((present * 100) / total,2),
            "students": students,
            "students_present": students_present
        }
        return render(request, 'dashboard.html',context)
    return render(request, 'dashboard.html',{"total":total})

def registered_students(request):

    students = Register.objects.all()

    return render(request, 'registered_students.html', {"students": students})