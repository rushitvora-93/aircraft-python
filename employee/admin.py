from django.contrib import admin
from .models import Employee_Status
from django.contrib.auth.models import User, Group


class Employee_Status_Admin(admin.ModelAdmin):
    list_display = ('employee_number', 'booking_status', 'present_status', 'updated_at')
    list_filter = ('booking_status', 'present_status')


admin.site.register(Employee_Status, Employee_Status_Admin)
admin.site.unregister(User)
admin.site.unregister(Group)
