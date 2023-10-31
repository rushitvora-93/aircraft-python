from django.urls import path
from .views import partNumberTracker

app_name = 'material'

urlpatterns = [
    path('partNumberTracker/', partNumberTracker.as_view(), name='partNumberTracker'),
]