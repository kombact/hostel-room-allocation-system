from django.contrib import admin
from .models import Student, Room, Allocation, WaitlistEntry
# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('rollno', 'name','age','gender','email','course','year','contact_number')
    search_fields = ('rollno', 'name', 'email')
    list_filter = ('gender','course', 'year')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'block',  'gender_type', 'capacity', 'current_occupancy', 'is_available']
    search_fields = ['room_number', 'block']
    list_filter = ['block', 'gender_type']


@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ['student', 'room', 'status', 'allocated_on','vacated_date']
    search_fields = ['student__name', 'room__room_number']
    list_filter = ['status', 'room__block']


@admin.register(WaitlistEntry)
class WaitlistAdmin(admin.ModelAdmin):
    list_display = ['student', 'requested_date', 'priority']
    search_fields = ['student__name']
    list_filter = ['requested_date']