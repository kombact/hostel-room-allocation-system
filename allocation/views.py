from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Student, Room, Allocation, WaitlistEntry

@login_required
def dashboard(request):
    total_rooms = Room.objects.count()
    total_students = Student.objects.count()
    active_allocations = Allocation.objects.filter(status='Active').count()
    waitlist_count = WaitlistEntry.objects.count()

    all_rooms = Room.objects.all()
    available_rooms = sum(1 for room in all_rooms if room.is_available())
    occupied_rooms = total_rooms - available_rooms

    context = {
        'total_rooms': total_rooms,
        'total_students': total_students,
        'active_allocations': active_allocations,
        'waitlist_count': waitlist_count,
        'available_rooms': available_rooms,
        'occupied_rooms': occupied_rooms,
        'recent_allocations': Allocation.objects.select_related('student', 'room').order_by('-allocated_date')[:5],  # ← this is the line
    }
    return render(request, 'allocation/dashboard.html', context)