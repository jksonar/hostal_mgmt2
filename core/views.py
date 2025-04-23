from .forms import UserRegisterForm, RoomRequestForm
from .models import StudentProfile, TeacherProfile, RoomRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import RoomRequest
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
# from django.http import HttpResponse

def home(request):
    return render(request,'base.html')

@login_required
def request_room(request):
    user = request.user
    profile = None
    is_student = False
    is_teacher = False

    if hasattr(user, 'studentprofile'):
        profile = user.studentprofile
        is_student = True
    elif hasattr(user, 'teacherprofile'):
        profile = user.teacherprofile
        is_teacher = True

    if request.method == 'POST':
        form = RoomRequestForm(request.POST)
        if form.is_valid():
            room_request = form.save(commit=False)
            if is_student:
                room_request.student = profile
            elif is_teacher:
                room_request.teacher = profile
            room_request.save()
            return redirect('home')
    else:
        form = RoomRequestForm()

    return render(request, 'core/request_room.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Check profile type and redirect
            if hasattr(user, 'studentprofile'):
                return redirect('student_dashboard')
            elif hasattr(user, 'teacherprofile'):
                return redirect('teacher_dashboard')
            else:
                return redirect('home')  # Fallback redirect
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def student_dashboard(request):
    profile = request.user.studentprofile
    latest_request = RoomRequest.objects.filter(student=profile).order_by('-requested_at').first()
    
    allow_request = (
        not latest_request or
        latest_request.status == 'rejected'
    )

    if request.method == 'POST':
        if allow_request:
            form = RoomRequestForm(request.POST)
            if form.is_valid():
                room_request = form.save(commit=False)
                room_request.student = profile
                room_request.save()
                return redirect('student_dashboard')
        else:
            form = RoomRequestForm()
            form.add_error(None, "You can't submit another request right now.")
    else:
        form = RoomRequestForm()

    return render(request, 'core/student_dashboard.html', {
        'profile': profile,
        'form': form,
        'latest_request': latest_request,
        'allow_request': allow_request
    })

@login_required
def teacher_dashboard(request):
    profile = request.user.teacherprofile
    latest_request = RoomRequest.objects.select_related('student').order_by('-requested_at').first()

    allow_request = (
        not latest_request or
        latest_request.status == 'rejected'
    )

    if request.method == 'POST':
        if allow_request:
            form = RoomRequestForm(request.POST)
            if form.is_valid():
                room_request = form.save(commit=False)
                room_request.teacher = profile
                room_request.save()
                return redirect('teacher_dashboard')
        else:
            form = RoomRequestForm()
            form.add_error(None, "You can't submit another request right now.")
    else:
        form = RoomRequestForm()

    return render(request, 'core/teacher_dashboard.html', {
        'profile': profile,
        'form': form,
        'latest_request': latest_request,
        'allow_request': allow_request
    })

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            is_student = form.cleaned_data.get('is_student')
            is_teacher = form.cleaned_data.get('is_teacher')

            if is_student:
                StudentProfile.objects.create(user=user, roll_number=form.cleaned_data.get('roll_number'))
            if is_teacher:
                TeacherProfile.objects.create(user=user)

            messages.success(request, 'Account created successfully.')
            return redirect('login')  # 🔁 avoid resubmission on reload
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            StudentProfile.objects.create(
                user=user,
                roll_number=form.cleaned_data['roll_number']
            )
            # Proceed with login or redirect
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    requests = RoomRequest.objects.select_related('student__user', 'teacher__user', 'room').order_by('-requested_at')
    return render(request, 'admin/dashboard.html', {'requests': requests})

@user_passes_test(is_admin)
def approve_request(request, pk):
    room_request = get_object_or_404(RoomRequest, pk=pk)
    room_request.status = 'approved'
    room_request.save()
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def reject_request(request, pk):
    room_request = get_object_or_404(RoomRequest, pk=pk)
    room_request.status = 'rejected'
    room_request.save()
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def delete_request(request, pk):
    room_request = get_object_or_404(RoomRequest, pk=pk)
    room_request.delete()
    return redirect('admin_dashboard')
