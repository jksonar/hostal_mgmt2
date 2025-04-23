from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('request-room/', views.request_room, name='request_room'),
    path('login/', views.user_login, name='login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('site-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('site-admin/room-request/<int:pk>/approve/', views.approve_request, name='approve_request'),
    path('site-admin/room-request/<int:pk>/reject/', views.reject_request, name='reject_request'),
    path('site-admin/room-request/<int:pk>/delete/', views.delete_request, name='delete_request'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
