from django.db import models

# Create your models here.

class Employee_Status(models.Model):
    PRESENT_STATUS_CHOICES = (
        ('present', 'present'),
        ('absent', 'absent')
    )

    employee_number = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    booking_status = models.BooleanField(default=True)
    present_status = models.CharField(max_length=50, choices=PRESENT_STATUS_CHOICES, default="Absent")
    updated_at = models.DateTimeField(auto_now=True)