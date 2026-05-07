from django.db import models

class Student(models.Model):
    GENDER= [("MALE","MALE"),("FEMALE","FEMALE")]
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender=models.CharField(max_length=10, choices=GENDER)
    email = models.EmailField(unique=True)
    roll_number = models.IntegerField(unique=True)
    course = models.CharField(max_length=100)
    year = models.IntegerField()
    contact = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.rollno} - {self.name}"

class Room(models.Model):
    ROOM_TYPE_CHOICES = [('Single', 'Single'), ('Double', 'Double'), ('Triple', 'Triple')]
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]

    room_number = models.CharField(max_length=10, unique=True)
    block = models.CharField(max_length=10)
    floor = models.PositiveIntegerField()
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    gender_type = models.CharField(max_length=10, choices=GENDER_CHOICES)
    capacity = models.PositiveIntegerField()
    
    def current_occupancy(self):
        return self.allocation_set.filter(status='Allocated').count()

    def is_available(self):
        return self.current_occupancy() < self.capacity

    def __str__(self):
        return f"Room {self.room_number} - Block {self.block}"
    
class Allocation(models.Model):
    STATUS = [("ALLOCATED","ALLOCATED"),("VACANT","VACANT")]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS, default="ALLOCATED")
    allocated_date = models.DateTimeField(auto_now_add=True)
    vacated_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.rollno}-{self.student.name} allocated to {self.room.room_number}"
class WaitlistEntry(models.Model):
    
    ROOM_TYPE_CHOICES = [('Single', 'Single'), ('Double', 'Double'), ('Triple', 'Triple')]

    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    preferred_room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    requested_date = models.DateField(auto_now_add=True)
    priority = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['priority', 'requested_date']

    def __str__(self):
        return f"Waitlist: {self.student.name} ({self.student.rollno})"