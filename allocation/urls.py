from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='allocation/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='allocation/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Rooms
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.room_add, name='room_add'),
    path('rooms/<int:pk>/edit/', views.room_edit, name='room_edit'),
    path('rooms/<int:pk>/delete/', views.room_delete, name='room_delete'),
    
    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    
    # Allocations
    path('allocations/', views.allocation_list, name='allocation_list'),
    path('allocations/allocate/', views.allocate_room, name='allocate_room'),
    path('allocations/<int:pk>/vacate/', views.vacate_room, name='vacate_room'),
    # Waitlist
    path('waitlist/', views.waitlist, name='waitlist'),
    path('waitlist/add/', views.waitlist_add, name='waitlist_add'),
    path('waitlist/<int:pk>/remove/', views.waitlist_remove, name='waitlist_remove'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
    path('reports/export/allocations/', views.export_allocations_csv, name='export_allocations'),
    path('reports/export/students/', views.export_students_csv, name='export_students'),
    path('reports/export/waitlist/', views.export_waitlist_csv, name='export_waitlist'),
]