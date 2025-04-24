from django.contrib import admin
from .models import Profile, Room, RoomRequest

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'is_verified')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'available')

@admin.register(RoomRequest)
class RoomRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'duration', 'status', 'created_at')
