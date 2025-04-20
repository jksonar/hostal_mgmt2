from .forms import RoomRequestForm
from .models import RoomRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RoomRequestForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Hostel Management System")

def request_room(request):
    if request.method == 'POST':
        form = RoomRequestForm(request.POST)
        if form.is_valid():
            form.save()
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


