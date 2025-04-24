from django import forms
from django.contrib.auth.models import User
from .models import Profile, Room, RoomRequest
from django.contrib.auth.forms import UserCreationForm

# User Registration Form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)
    id_proof = forms.FileField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'id_proof']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = Profile.objects.get(user=user)
            profile.role = self.cleaned_data['role']
            profile.id_proof = self.cleaned_data['id_proof']
            profile.save()
        return user

# Room Form (for Admin)
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'available']

# Room Request Form (for verified users)
class RoomRequestForm(forms.ModelForm):
    class Meta:
        model = RoomRequest
        fields = ['room', 'duration']
        widgets = {
            'duration': forms.Select(choices=RoomRequest.DURATION_CHOICES),
        }
