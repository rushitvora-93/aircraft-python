from django.urls import path
from .views import getEmployee, getPhase, getMaterialMovementType #verifyWorkOrder

app_name = 'fatchData'

urlpatterns = [
    path('getEmployee/', getEmployee.as_view(), name='get_employee'),
    path('getPhase/', getPhase.as_view(), name='get_phase'),
    # path('verifyWorkOrder/', verifyWorkOrder.as_view(), name='verify_work_order'),
    path('getMaterialMovementType/', getMaterialMovementType.as_view(), name='get_material_movement_type')
]