from django.db import models

# Create your models here.

class Material_Movement_Log(models.Model):
    EXCEPTION_CHOICES = (
        ('yes', 'yes'),
        ('no', 'no')
    )
    work_order = models.CharField(max_length=100)
    requirement_number = models.CharField(max_length=100)
    aircraft_registration = models.CharField(max_length=100)
    required_by = models.CharField(max_length=100)
    hi_pick = models.CharField(max_length=100)
    part_number = models.CharField(max_length=100)
    part_description = models.CharField(max_length=300)
    quantity = models.CharField(max_length=100)
    required_quantity = models.CharField(max_length=100)
    issued_quantity = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    exception = models.CharField(choices=EXCEPTION_CHOICES, default="no", max_length=100)
    material_movement_id_type = models.CharField(max_length=100)
    employee_number = models.CharField(max_length=100)
    event_date_time = models.DateTimeField(auto_now_add=True, max_length=100)
    movement_type = models.CharField(max_length=100)

