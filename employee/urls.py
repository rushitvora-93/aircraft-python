from django.contrib import admin
from django.urls import path
from .views import employeeStatusView

app_name = 'employee'

urlpatterns = [
    path('employeeStatus/', employeeStatusView.as_view(), name='employee_status'),
]