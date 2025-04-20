from django.contrib import admin
from .models import Room, Student, Teacher
from .models import RoomRequest
from django.urls import path
from django.contrib import admin
from django.shortcuts import render, redirect, get_object_or_404
from .models import RoomRequest, Room, Student, Teacher
from django import forms

# @admin.register(RoomRequest)
# class RoomRequestAdmin(admin.ModelAdmin):
#     list_display = ('student', 'teacher', 'status', 'room', 'requested_at')
#     list_filter = ('status',)

admin.site.register(Room)
admin.site.register(Student)
admin.site.register(Teacher)


class RoomAllocationForm(forms.Form):
    room = forms.ModelChoiceField(queryset=Room.objects.all())

# Custom admin view
def allocate_room_view(request, request_id):
    room_request = get_object_or_404(RoomRequest, id=request_id)
    if request.method == 'POST':
        form = RoomAllocationForm(request.POST)
        if form.is_valid():
            room = form.cleaned_data['room']
            room_request.room = room
            room_request.status = 'approved'

            if room_request.student:
                room_request.student.room = room
                room_request.student.save()
            elif room_request.teacher:
                room_request.teacher.room = room
                room_request.teacher.save()

            room_request.save()
            return redirect('..')  # back to admin list
    else:
        form = RoomAllocationForm()

    return render(request, 'admin/allocate_room.html', {
        'form': form,
        'room_request': room_request
    })

# Custom Admin Class
class RoomRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher', 'status', 'room', 'requested_at')
    change_list_template = "admin/room_request_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'allocate/<int:request_id>/',
                self.admin_site.admin_view(allocate_room_view),
                name='allocate_room',
            ),
        ]
        return custom_urls + urls

admin.site.register(RoomRequest, RoomRequestAdmin)
