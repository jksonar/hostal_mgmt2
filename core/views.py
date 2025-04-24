from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Profile
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserRegisterForm, RoomForm, RoomRequestForm
from .models import Profile, Room, RoomRequest
from django.contrib import messages

def is_admin(user):
    return hasattr(user, 'profile') and user.profile.role == 'admin'

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        role = request.POST.get('role')
        id_proof = request.FILES.get('id_proof')

        if form.is_valid():
            user = form.save()

            try:
                # Only create Profile if one doesn't exist
                profile, created = Profile.objects.get_or_create(
                    user=user,
                    defaults={'role': role, 'id_proof': id_proof}
                )
                if not created:
                    profile.role = role
                    profile.id_proof = id_proof
                    profile.save()

            except IntegrityError:
                messages.error(request, 'A profile for this user already exists.')
                return redirect('register')  # or wherever appropriate

            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        # Optional: auto-create for admin
        profile = Profile.objects.create(user=request.user, role='admin', id_proof='id_proofs/default.pdf', is_verified=True)
    
    if profile.role == 'admin':
        return redirect('admin_dashboard')
    return render(request, 'core/user_dashboard.html')

@login_required
def room_request_view(request):
    if not request.user.profile.is_verified:
        return render(request, 'core/unverified.html')
    if RoomRequest.objects.filter(user=request.user, status__in=['pending', 'approved']).exists():
        messages.warning(request, "You already have an active room request.")
        return redirect('dashboard')
    if request.method == 'POST':
        form = RoomRequestForm(request.POST)
        if form.is_valid():
            room_request = form.save(commit=False)
            room_request.user = request.user
            room_request.save()
            messages.success(request, "Room request sent.")
            return redirect('dashboard')
    else:
        form = RoomRequestForm()
    return render(request, 'core/room_request.html', {'form': form})

@login_required
def cancel_room_request(request, pk):
    room_request = get_object_or_404(RoomRequest, pk=pk, user=request.user)
    if room_request.status == 'pending':
        room_request.status = 'cancelled'
        room_request.save()
        messages.success(request, "Room request cancelled.")
    return redirect('dashboard')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    users = Profile.objects.exclude(role='admin')
    rooms = Room.objects.all()
    requests = RoomRequest.objects.all()
    return render(request, 'core/admin_dashboard.html', {
        'users': users,
        'rooms': rooms,
        'requests': requests
    })

@login_required
@user_passes_test(is_admin)
def verify_user(request, user_id):
    profile = get_object_or_404(Profile, id=user_id)
    profile.is_verified = True
    profile.save()
    return redirect('admin_dashboard')

@login_required
@user_passes_test(is_admin)
def manage_room(request, room_id=None):
    room = None
    if room_id:
        room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = RoomForm(instance=room)
    return render(request, 'core/room_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.delete()
    return redirect('admin_dashboard')

@login_required
@user_passes_test(is_admin)
def update_request_status(request, request_id, status):
    room_request = get_object_or_404(RoomRequest, id=request_id)
    if status in ['approved', 'rejected', 'pending']:
        room_request.status = status
        room_request.save()
    return redirect('admin_dashboard')

@login_required
def request_detail_view(request, request_id):
    room_request = get_object_or_404(RoomRequest, id=request_id, user=request.user)
    occupants = RoomRequest.objects.filter(room=room_request.room, status='approved').exclude(user=request.user)
    return render(request, 'core/request_detail.html', {
        'request': room_request,
        'occupants': occupants
    })

@login_required
def available_rooms(request):
    if not request.user.profile.is_verified:
        return render(request, 'core/unverified.html')
    rooms = Room.objects.filter(available=True)
    return render(request, 'core/available_rooms.html', {'rooms': rooms})
