from rest_framework import serializers
from .models import Material_Movement_Log

class Material_Movement_Log_Post_Serializer(serializers.ModelSerializer):

    id = serializers.CharField(read_only=True, required=False)
    work_order = serializers.CharField(read_only=False, required=True)
    requirement_number = serializers.CharField(read_only=False, required=True)
    aircraft_registration = serializers.CharField(read_only=False, required=True)
    required_by = serializers.CharField(read_only=False, required=True)
    hi_pick = serializers.CharField(read_only=False, required=True)
    part_number = serializers.CharField(read_only=False, required=True)
    part_description = serializers.CharField(read_only=False, required=True)
    quantity = serializers.CharField(read_only=False, required=True)
    required_quantity = serializers.CharField(read_only=False, required=True)
    issued_quantity = serializers.CharField(read_only=False, required=True)
    status = serializers.CharField(read_only=False, required=True)
    exception = serializers.ChoiceField(choices=Material_Movement_Log.EXCEPTION_CHOICES, read_only=False, required=False)
    material_movement_id_type = serializers.CharField(read_only=False, required=True)
    employee_number = serializers.CharField(read_only=False, required=True)
    event_date_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, required=False)
    movement_type = serializers.CharField(read_only=False, required=True)


    class Meta:
        model = Material_Movement_Log
        fields = ['id', 'work_order', 'requirement_number', 'aircraft_registration', 'required_by', 'hi_pick', 'part_number', 'part_description', 'quantity', 'required_quantity', 'issued_quantity', 'status', 'exception', 'material_movement_id_type', 'employee_number', 'event_date_time', 'movement_type']


class Material_Movement_Log_Patch_Serializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=False, required=True)
    quantity = serializers.CharField(read_only=False, required=True)
    exception = serializers.ChoiceField(choices=Material_Movement_Log.EXCEPTION_CHOICES, read_only=False, required=False)
    
    class Meta:
        model = Material_Movement_Log
        fields = ['id', 'quantity', 'exception']