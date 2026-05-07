from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'block', 'floor', 'room_type', 'gender_type', 'capacity']
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'block': forms.TextInput(attrs={'class': 'form-control'}),
            'floor': forms.NumberInput(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-select'}),
            'gender_type': forms.Select(attrs={'class': 'form-select'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
from .models import Room, Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'gender', 'course', 'year', 'contact', 'email', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'roll_number': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

from .models import Room, Student, Allocation

class AllocationForm(forms.ModelForm):
    class Meta:
        model = Allocation
        fields = ['student', 'room']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'room': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show students who are not already allocated
        allocated_student_ids = Allocation.objects.filter(status='Active').values_list('student_id', flat=True)
        self.fields['student'].queryset = Student.objects.exclude(id__in=allocated_student_ids)
        # Only show available rooms
        self.fields['room'].queryset = Room.objects.all()


from .models import Room, Student, Allocation, WaitlistEntry

class WaitlistForm(forms.ModelForm):
    class Meta:
        model = WaitlistEntry
        fields = ['student', 'preferred_room_type', 'priority']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'preferred_room_type': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show students not already allocated or on waitlist
        allocated_ids = Allocation.objects.filter(status='Active').values_list('student_id', flat=True)
        waitlisted_ids = WaitlistEntry.objects.values_list('student_id', flat=True)
        self.fields['student'].queryset = Student.objects.exclude(id__in=allocated_ids).exclude(id__in=waitlisted_ids)       