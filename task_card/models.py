from django.db import models

# Create your models here.

class Task_Card_Log(models.Model):
    NRC_CHOICES = (
        ('yes', 'yes'),
        ('no', 'no')
    )
    STATUS_CHOICES = (
        ('open', 'open'),
        ('closed', 'closed'),
        ('canceled', 'canceled')
    )
    task_card_barcode = models.CharField(max_length=200)
    work_order = models.CharField(max_length=100, null=True)
    task_card_number = models.CharField(max_length=100)
    nrc = models.CharField(max_length=100, choices=NRC_CHOICES, null=True)
    location = models.CharField(max_length=100, null=True)
    time_phase = models.CharField(max_length=100, null=True)
    production_phase = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    remark = models.CharField(max_length=300, null=True, blank=True)
    employee_number = models.CharField(max_length=100)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=None, null=True, blank=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(default=None, null=True, blank=True)
    worked = models.CharField(choices=NRC_CHOICES, default="yes", max_length=100)
    status = models.CharField(choices=STATUS_CHOICES, default="open", max_length=100)
    calculated_time = models.TimeField(default=None, null=True, blank=True)