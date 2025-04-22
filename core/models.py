from django.contrib.auth.models import User
from django.db import models

def user_profile_picture_path(instance, filename):
    # upload path will be: media/profile_pictures/user_<id>/<filename>
    return f'profile_pictures/user_{instance.user.id}/{filename}'

class Room(models.Model):
    number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField()
    is_teacher_room = models.BooleanField(default=False)

    def __str__(self):
        return f"Room {self.number}"

class RoomRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey('TeacherProfile', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.student or self.teacher} - {self.status}"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True, blank=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, null=True, blank=True)

    def __str__(self):
        return self.user.username

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True, blank=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, null=True, blank=True)

    def __str__(self):
        return self.user.username
