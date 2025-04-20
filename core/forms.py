from django import forms
from .models import RoomRequest

class RoomRequestForm(forms.ModelForm):
    class Meta:
        model = RoomRequest
        # fields = ['student', 'teacher']  # One of them will be filled based on user type
        fields = []  # We will set student/teacher in the view
