from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('room/request/', views.room_request_view, name='room_request'),
    path('room/cancel/<int:pk>/', views.cancel_room_request, name='cancel_request'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/verify/<int:user_id>/', views.verify_user, name='verify_user'),
    path('admin/room/add/', views.manage_room, name='add_room'),
    path('admin/room/edit/<int:room_id>/', views.manage_room, name='edit_room'),
    path('admin/room/delete/<int:room_id>/', views.delete_room, name='delete_room'),
    path('admin/request/<int:request_id>/<str:status>/', views.update_request_status, name='update_request_status'),
]
