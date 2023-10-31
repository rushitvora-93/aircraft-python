from rest_framework import serializers
from .models import Task_Card_Log

class Task_Card_Log_Post_Serializer(serializers.ModelSerializer):

    id = serializers.CharField(read_only=True, required=False)
    task_card_barcode = serializers.CharField(read_only=False, required=True)
    work_order = serializers.CharField(read_only=False, required=False)
    task_card_number = serializers.CharField(read_only=False, required=False)
    nrc = serializers.ChoiceField(choices=Task_Card_Log.NRC_CHOICES, read_only=False, required=False)
    location = serializers.CharField(read_only=False, required=False)
    time_phase = serializers.CharField(read_only=False, required=False)
    production_phase = serializers.CharField(read_only=False, required=False)
    title = serializers.CharField(read_only=False, required=False)
    remark = serializers.CharField(read_only=False, required=False)
    employee_number = serializers.CharField(read_only=False, required=True)
    start_date = serializers.DateField(format='%Y-%m-%d', read_only=True)
    end_date = serializers.DateField(format='%Y-%m-%d', read_only=False, required=False)
    start_time = serializers.TimeField(format='%H:%M:%S', read_only=False, required=False)
    end_time = serializers.TimeField(format='%H:%M:%S', read_only=False, required=False)
    calculated_time = serializers.TimeField(format='%H:%M:%S', read_only=False, required=False)
    worked = serializers.ChoiceField(choices=Task_Card_Log.NRC_CHOICES, read_only=False, required=False)
    status = serializers.ChoiceField(choices=Task_Card_Log.STATUS_CHOICES, read_only=False, required=False)

    class Meta:
        model = Task_Card_Log
        fields = ['id', 'task_card_barcode', 'work_order', 'task_card_number', 'nrc', 'location', 'time_phase', 'production_phase', 'title', 'remark', 'employee_number', 'start_date', 'end_date', 'start_time', 'end_time', 'calculated_time', 'worked', 'status']

class Task_Card_Log_Patch_Serializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=False, required=True)
    title = serializers.CharField(read_only=False, required=False)
    remark = serializers.CharField(read_only=False, required=False)
    end_date = serializers.DateField(format='%Y-%m-%d', read_only=False, required=False)
    end_time = serializers.TimeField(format='%H:%M:%S', read_only=False, required=False)
    calculated_time = serializers.TimeField(format='%H:%M:%S', read_only=False, required=False)
    worked = serializers.ChoiceField(choices=Task_Card_Log.NRC_CHOICES, read_only=False, required=False)
    status = serializers.ChoiceField(choices=Task_Card_Log.STATUS_CHOICES, read_only=False, required=False)

    class Meta:
        model = Task_Card_Log
        fields = ['id', 'title', 'remark', 'end_date', 'end_time', 'calculated_time', 'worked', 'status']
