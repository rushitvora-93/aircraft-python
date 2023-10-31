from rest_framework import serializers
from .models import Employee_Status

class Employee_Status_Serializer(serializers.ModelSerializer):

    id = serializers.CharField(read_only=True, required=False)
    employee_number = serializers.CharField(read_only=False, required=True)
    first_name = serializers.CharField(read_only=False, required=False)
    surname = serializers.CharField(read_only=False, required=False)
    booking_status = serializers.BooleanField(read_only=False, required=True)
    present_status = serializers.ChoiceField(choices=Employee_Status.PRESENT_STATUS_CHOICES,read_only=False, required=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Employee_Status
        fields = ['id', 'employee_number', 'first_name', 'surname', 'booking_status', 'present_status', 'updated_at']
