from rest_framework.views import APIView
from rest_framework.response import Response
from error_handling.error_handler import handle_error
from response_handling.response_handler import handle_response
from .utils import execute_query
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class getEmployee(APIView):
    #get employee data
    @swagger_auto_schema(manual_parameters=[openapi.Parameter('employeeName', openapi.IN_QUERY, type=openapi.TYPE_STRING)],  operation_summary="Get Employee Status By Employee Name")
    def get(self, request):
        employee_name = request.GET.get('employeeName', None)
        if employee_name:
            query = "SELECT * FROM employee_employee_status WHERE first_name LIKE '%{}%'".format(employee_name)
            response_data = execute_query(query)
        else:
            query = "SELECT * FROM employee_employee_status"
            response_data = execute_query(query)
        
        if len(response_data) < 1:
            response_data = handle_error("Data Not Found", 404)
            return Response(response_data, 404)
        response_data = handle_response(response_data, "success", 200, len(response_data))
        return Response(response_data, content_type='application/json')


class getPhase(APIView):
    def get_location(self, response_data):
        # query = "SELECT * FROM location"
        # query_data = execute_query(query)
        response_data['locations'] = [{"id": "1", "location":"location - 1"},{"id": "2", "location":"location - 2"},{"id": "3", "location":"location - 3"}]
        return response_data
    
    def get_time_phase(self, response_data):
        # query = "SELECT * FROM time_phase"
        # query_data = execute_query(query)
        response_data['time_phase'] = [{"id": "1", "time_phase":"time_phase - 1"},{"id": "2", "time_phase":"time_phase - 2"},{"id": "3", "time_phase":"time_phase - 3"}]
        return response_data
    
    def get_production_phase(self, response_data):
        # query = "SELECT * FROM production_phase"
        # query_data = execute_query(query)
        response_data['production_phase'] = [{"id": "1", "production_phase":"production_phase - 1"},{"id": "2", "production_phase":"production_phase - 2"},{"id": "3", "production_phase":"production_phase - 3"}]
        return response_data

    #get phase data
    def get(self, request):
        response_data = {}
        response_data = self.get_location(response_data)
        response_data = self.get_time_phase(response_data)
        response_data = self.get_production_phase(response_data)

        if len(response_data) < 1:
            response_data = handle_error("Data Not Found", 404)
            return Response(response_data, 404)

        response_data = handle_response(response_data, "success", 200, len(response_data))
        return Response(response_data, content_type='application/json')


# Validate Work Order
# class verifyWorkOrder(APIView):
#     #get employee data
#     @swagger_auto_schema(manual_parameters=[openapi.Parameter('workOrder', openapi.IN_QUERY, type=openapi.TYPE_STRING)],  operation_summary="Verify Work Order")
#     def get(self, request):
#         work_order = request.GET.get('workOrder', None)
#         if work_order:
#             query = "SELECT * FROM work_order WHERE work_order=work_order"
#             response_data = execute_query(query)
#             if len(response_data) < 1:
#                 response_data = handle_error("Wrong Work Order", 400)
#                 return Response(response_data, 404)
#             response_data = handle_response("Work Order Is Valid", "success", 200, len(response_data))
#             return Response(response_data, content_type='application/json')
#         else:
#             response_data = handle_error("Invalid Work Order", 400)
#             return Response(response_data, 400)


class getMaterialMovementType(APIView):
    def get(self, request):
        # query = "SELECT * FROM material_movement_type"
        # response_data = execute_query(query)
        response_data = [{"id": "1", "movement_type":"movement_type - 1"},{"id": "2", "movement_type":"movement_type - 2"},{"id": "3", "movement_type":"movement_type - 3"}]

        if len(response_data) < 1:
            response_data = handle_error("Data Not Found", 404)
            return Response(response_data, 404)

        response_data = handle_response(response_data, "success", 200, len(response_data))
        return Response(response_data, content_type='application/json')