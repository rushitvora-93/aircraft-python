from django.contrib import admin
from .models import Task_Card_Log

class Task_Card_Log_Admin(admin.ModelAdmin):
    list_display = ('task_card_number', 'task_card_barcode', 'employee_number', 'start_date')
    list_display_links = ['task_card_number']
    list_filter = ('employee_number', 'start_date')


admin.site.register(Task_Card_Log, Task_Card_Log_Admin)