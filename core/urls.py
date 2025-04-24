from django.urls import path
from . import views
from .views import available_rooms, request_detail_view
# from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('accounts/login/', auth_views.LoginView.as_view(), name='account_login'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('room/request/', views.room_request_view, name='room_request'),
    path('room/cancel/<int:pk>/', views.cancel_room_request, name='cancel_request'),
    path('site-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('site-admin/verify/<int:user_id>/', views.verify_user, name='verify_user'),
    path('site-admin/room/add/', views.manage_room, name='add_room'),
    path('site-admin/room/edit/<int:room_id>/', views.manage_room, name='edit_room'),
    path('site-admin/room/delete/<int:room_id>/', views.delete_room, name='delete_room'),
    path('site-admin/request/<int:request_id>/<str:status>/', views.update_request_status, name='update_request_status'),
    path('available-rooms/', available_rooms, name='available_rooms'),
    path('request/<int:request_id>/', request_detail_view, name='request_detail'),
]
