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

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import RoomForm

@login_required
def room_list(request):
    rooms = Room.objects.all().order_by('block', 'room_number')
    return render(request, 'allocation/room_list.html', {'rooms': rooms})

@login_required
def room_add(request):
    form = RoomForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Room added successfully.')
        return redirect('room_list')
    return render(request, 'allocation/room_form.html', {'form': form, 'title': 'Add Room'})

@login_required
def room_edit(request, pk):
    room = get_object_or_404(Room, pk=pk)
    form = RoomForm(request.POST or None, instance=room)
    if form.is_valid():
        form.save()
        messages.success(request, 'Room updated successfully.')
        return redirect('room_list')
    return render(request, 'allocation/room_form.html', {'form': form, 'title': 'Edit Room'})

@login_required
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Room deleted successfully.')
        return redirect('room_list')
    return render(request, 'allocation/room_confirm_delete.html', {'room': room})
@login_required
def student_list(request):
    students = Student.objects.all().order_by('name')
    return render(request, 'allocation/student_list.html', {'students': students})

@login_required
def student_add(request):
    form = StudentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Student added successfully.')
        return redirect('student_list')
    return render(request, 'allocation/student_form.html', {'form': form, 'title': 'Add Student'})

@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, request.FILES or None, instance=student)
    if form.is_valid():
        form.save()
        messages.success(request, 'Student updated successfully.')
        return redirect('student_list')
    return render(request, 'allocation/student_form.html', {'form': form, 'title': 'Edit Student'})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('student_list')
    return render(request, 'allocation/student_confirm_delete.html', {'student': student})

@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    allocation = Allocation.objects.filter(student=student).first()
    return render(request, 'allocation/student_detail.html', {'student': student, 'allocation': allocation})

from .models import Student, Room, Allocation, WaitlistEntry
from .forms import RoomForm, StudentForm, AllocationForm
from django.utils import timezone

@login_required
def allocation_list(request):
    allocations = Allocation.objects.select_related('student', 'room').order_by('-allocated_date')
    return render(request, 'allocation/allocation_list.html', {'allocations': allocations})


@login_required
def allocate_room(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        room_id = request.POST.get('room')

        student = get_object_or_404(Student, pk=student_id)
        room = get_object_or_404(Room, pk=room_id)

        # Check gender match
        if student.gender != room.gender_type:
            messages.error(request, f'Gender mismatch! {student.name} is {student.gender} but room is for {room.gender_type} students.')
            return redirect('allocate_room')

        # Check room availability
        if not room.is_available():
            # Add to waitlist
            if not WaitlistEntry.objects.filter(student=student).exists():
                WaitlistEntry.objects.create(
                    student=student,
                    preferred_room_type=room.room_type,
                )
                messages.warning(request, f'Room is full. {student.name} has been added to the waitlist.')
            else:
                messages.warning(request, f'{student.name} is already on the waitlist.')
            return redirect('allocation_list')

        # Allocate room
        Allocation.objects.create(student=student, room=room)

        # Remove from waitlist if they were on it
        WaitlistEntry.objects.filter(student=student).delete()

        messages.success(request, f'Room {room.room_number} successfully allocated to {student.name}.')
        return redirect('allocation_list')

    form = AllocationForm()
    return render(request, 'allocation/allocation_form.html', {'form': form})


@login_required
def vacate_room(request, pk):
    allocation = get_object_or_404(Allocation, pk=pk)
    if request.method == 'POST':
        allocation.status = 'Vacated'
        allocation.vacated_date = timezone.now().date()
        allocation.save()

        # Check waitlist — allocate to next student if room now available
        room = allocation.room
        if room.is_available():
            next_entry = WaitlistEntry.objects.filter(
                student__gender=room.gender_type,
                preferred_room_type=room.room_type
            ).first()

            if next_entry:
                Allocation.objects.create(student=next_entry.student, room=room)
                next_entry.delete()
                messages.success(request, f'Room vacated. Auto-allocated to waitlisted student {next_entry.student.name}.')
                return redirect('allocation_list')

        messages.success(request, f'Room vacated successfully.')
        return redirect('allocation_list')

    return render(request, 'allocation/vacate_confirm.html', {'allocation': allocation})
from .forms import RoomForm, StudentForm, AllocationForm, WaitlistForm

@login_required
def waitlist(request):
    entries = WaitlistEntry.objects.select_related('student').order_by('priority', 'requested_date')
    return render(request, 'allocation/waitlist.html', {'entries': entries})


@login_required
def waitlist_add(request):
    form = WaitlistForm(request.POST or None)
    if form.is_valid():
        student = form.cleaned_data['student']
        if WaitlistEntry.objects.filter(student=student).exists():
            messages.warning(request, f'{student.name} is already on the waitlist.')
        else:
            form.save()
            messages.success(request, f'{student.name} added to waitlist.')
        return redirect('waitlist')
    return render(request, 'allocation/waitlist_form.html', {'form': form})


@login_required
def waitlist_remove(request, pk):
    entry = get_object_or_404(WaitlistEntry, pk=pk)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Removed from waitlist.')
        return redirect('waitlist')
    return render(request, 'allocation/waitlist_confirm_delete.html', {'entry': entry})

import csv
from django.http import HttpResponse

@login_required
def reports(request):
    total_rooms = Room.objects.count()
    total_students = Student.objects.count()
    active_allocations = Allocation.objects.filter(status='Active').count()
    vacated_allocations = Allocation.objects.filter(status='Vacated').count()
    waitlist_count = WaitlistEntry.objects.count()

    all_rooms = Room.objects.all()
    available_rooms = sum(1 for room in all_rooms if room.is_available())
    occupied_rooms = total_rooms - available_rooms

    # Room type breakdown
    single_rooms = Room.objects.filter(room_type='Single').count()
    double_rooms = Room.objects.filter(room_type='Double').count()
    triple_rooms = Room.objects.filter(room_type='Triple').count()

    # Gender breakdown
    male_rooms = Room.objects.filter(gender_type='Male').count()
    female_rooms = Room.objects.filter(gender_type='Female').count()

    # Block wise occupancy
    blocks = Room.objects.values_list('block', flat=True).distinct()
    block_data = []
    for block in blocks:
        block_rooms = Room.objects.filter(block=block)
        occupied = sum(1 for r in block_rooms if not r.is_available())
        block_data.append({
            'block': block,
            'total': block_rooms.count(),
            'occupied': occupied,
            'available': block_rooms.count() - occupied,
        })

    context = {
        'total_rooms': total_rooms,
        'total_students': total_students,
        'active_allocations': active_allocations,
        'vacated_allocations': vacated_allocations,
        'waitlist_count': waitlist_count,
        'available_rooms': available_rooms,
        'occupied_rooms': occupied_rooms,
        'single_rooms': single_rooms,
        'double_rooms': double_rooms,
        'triple_rooms': triple_rooms,
        'male_rooms': male_rooms,
        'female_rooms': female_rooms,
        'block_data': block_data,
    }
    return render(request, 'allocation/reports.html', context)


@login_required
def export_allocations_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="allocations.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Roll Number', 'Gender', 'Course', 'Year', 'Room No', 'Block', 'Floor', 'Room Type', 'Allocated Date', 'Status'])

    allocations = Allocation.objects.select_related('student', 'room').all()
    for alloc in allocations:
        writer.writerow([
            alloc.student.name,
            alloc.student.roll_number,
            alloc.student.gender,
            alloc.student.course,
            alloc.student.year,
            alloc.room.room_number,
            alloc.room.block,
            alloc.room.floor,
            alloc.room.room_type,
            alloc.allocated_date,
            alloc.status,
        ])
    return response


@login_required
def export_students_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Roll Number', 'Gender', 'Course', 'Year', 'Contact', 'Email'])

    for student in Student.objects.all():
        writer.writerow([
            student.name,
            student.roll_number,
            student.gender,
            student.course,
            student.year,
            student.contact,
            student.email,
        ])
    return response


@login_required
def export_waitlist_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="waitlist.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Roll Number', 'Gender', 'Preferred Room Type', 'Priority', 'Requested Date'])

    for entry in WaitlistEntry.objects.select_related('student').all():
        writer.writerow([
            entry.student.name,
            entry.student.roll_number,
            entry.student.gender,
            entry.preferred_room_type,
            entry.priority,
            entry.requested_date,
        ])
    return response