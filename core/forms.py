from django import forms
from .models import RoomRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RoomRequestForm(forms.ModelForm):
    class Meta:
        model = RoomRequest
        # fields = ['student', 'teacher']  # One of them will be filled based on user type
        fields = []  # We will set student/teacher in the view

# forms.py
class UserRegisterForm(UserCreationForm):
    is_student = forms.BooleanField(required=False)
    is_teacher = forms.BooleanField(required=False)
    roll_number = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_student', 'is_teacher', 'roll_number']

    def clean_roll_number(self):
        roll = self.cleaned_data.get('roll_number')
        if roll and StudentProfile.objects.filter(roll_number=roll).exists():
            raise forms.ValidationError("A student with this roll number already exists.")
        return roll