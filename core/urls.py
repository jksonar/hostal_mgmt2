from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('request-room/', views.request_room, name='request_room'),
    path('login/', views.user_login, name='login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('register/', views.register, name='register'),
]
