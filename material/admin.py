from django.contrib import admin
from .models import Material_Movement_Log

class Material_Movement_Log_Admin(admin.ModelAdmin):
    list_display = ('work_order', 'requirement_number', 'aircraft_registration', 'event_date_time')
    list_filter = ('employee_number', 'event_date_time', 'exception')


admin.site.register(Material_Movement_Log, Material_Movement_Log_Admin)