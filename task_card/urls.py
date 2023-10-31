from django.contrib import admin
from django.urls import path
from .views import taskCardTracker 

app_name = 'taskCard'

urlpatterns = [
    path('taskCardTracker/', taskCardTracker.as_view(), name='task_card_tracker')
]
