from django import forms
from .models import RoomRequest
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StudentProfile, TeacherProfile
from django.core.exceptions import ValidationError

class RoomRequestForm(forms.ModelForm):
    class Meta:
        model = RoomRequest
        fields = ['student', 'teacher']  # One of them will be filled based on user type

# forms.py
class UserRegisterForm(UserCreationForm):
    roll_number = forms.CharField(max_length=20)

    def clean_roll_number(self):
        roll_number = self.cleaned_data['roll_number']
        if StudentProfile.objects.filter(roll_number=roll_number).exists():
            raise ValidationError("This roll number is already in use.")
        return roll_number