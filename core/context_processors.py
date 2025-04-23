from .models import StudentProfile, TeacherProfile

def profile_picture(request):
    if request.user.is_authenticated:
        try:
            if hasattr(request.user, 'studentprofile'):
                return {'profile_picture': request.user.studentprofile.profile_picture}
            elif hasattr(request.user, 'teacherprofile'):
                return {'profile_picture': request.user.teacherprofile.profile_picture}
        except (StudentProfile.DoesNotExist, TeacherProfile.DoesNotExist):
            pass
    return {'profile_picture': None}
