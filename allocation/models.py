from django.db import models

class Student(models.Model):
    GENDER= [("MALE","MALE"),("FEMALE","FEMALE")]
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender=models.CharField(max_length=10, choices=GENDER)
    email = models.EmailField(unique=True)
    rollno = models.IntegerField(unique=True)
    course = models.CharField(max_length=100)
    year = models.IntegerField()
    contact_number = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.rollno} - {self.name}"

class Room(models.Model):
    GENDER= [("MALE","MALE"),("FEMALE","FEMALE")]
    room_number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField()
    occupied = models.IntegerField(default=0)
    block = models.CharField(max_length=10)
    
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
    allocated_on = models.DateTimeField(auto_now_add=True)
    vacated_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.rollno}-{self.student.name} allocated to {self.room.room_number}"
class WaitlistEntry(models.Model):
    
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    requested_date = models.DateField(auto_now_add=True)
    priority = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['priority', 'requested_date']

    def __str__(self):
        return f"Waitlist: {self.student.name} ({self.student.rollno})"