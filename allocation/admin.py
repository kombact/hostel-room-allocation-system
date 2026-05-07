from django.contrib import admin
from .models import Student, Room, Allocation, WaitlistEntry

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'roll_number', 'gender', 'course', 'year', 'contact', 'email']
    search_fields = ['name', 'roll_number', 'email']
    list_filter = ['gender', 'course', 'year']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'block', 'floor', 'room_type', 'gender_type', 'capacity', 'current_occupancy', 'is_available']
    search_fields = ['room_number', 'block']
    list_filter = ['block', 'floor', 'room_type', 'gender_type']


@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ['student', 'room', 'allocated_date', 'status', 'vacated_date']
    search_fields = ['student__name', 'room__room_number']
    list_filter = ['status', 'room__block']


@admin.register(WaitlistEntry)
class WaitlistAdmin(admin.ModelAdmin):
    list_display = ['student', 'preferred_room_type', 'requested_date', 'priority']
    search_fields = ['student__name']
    list_filter = ['preferred_room_type']