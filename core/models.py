from django.db import models
from django.contrib.auth.models import User

# User Profile model
class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Administrator'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    id_proof = models.FileField(upload_to='id_proofs/')
    is_verified = models.BooleanField(default=False)

# Room model
class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    floor = models.IntegerField(default=1)
    available = models.BooleanField(default=True)
    is_shared = models.BooleanField(default=False)
    capacity = models.IntegerField(default=1)

    def current_occupants(self):
        return RoomRequest.objects.filter(room=self, status='approved')

# Room request model
class RoomRequest(models.Model):
    DURATION_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
