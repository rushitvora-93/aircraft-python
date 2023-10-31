from rest_framework.views import APIView
from rest_framework.response import Response
from error_handling.error_handler import handle_error
from .models import Employee_Status
from response_handling.response_handler import handle_response
from .serializer import Employee_Status_Serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class employeeStatusView(APIView):
    #Create A New Employee / Update Status Of Existing Employee
    @swagger_auto_schema(request_body=Employee_Status_Serializer, operation_summary="Create A New Employee / Update Status Of Existing Employee")
    def post(self, request):
        request_body = request.data
        serializers = Employee_Status_Serializer(data = request_body)
        
        #validate input data
        if serializers.is_valid():
            if Employee_Status.objects.filter(employee_number = request_body['employee_number']).exists():

                try:
                    employee = Employee_Status.objects.get(employee_number = request_body['employee_number'])
                    employee.present_status = request_body['present_status']
                    employee.booking_status = request_body['booking_status']
                    employee.save()
                except Exception as error:
                    response_data = handle_error(str(error), 500)
                    return Response(response_data, 500)

                response_data = handle_response("Employee Status Updated", "success", 200, 1)
                return Response(response_data, 200)

            try:
                serializers.save()
            except Exception as error:
                response_data = handle_error(str(error), 500)
                return Response(response_data, 500)

            response_data = handle_response("Data Saved", "success", 200, 1)
            return Response(response_data, 200)

        else:
            err = list(serializers.errors)
            response_data = handle_error(f"Fields Missing/Invalid : {err}", 400)
            return Response(response_data, 400)
    
    # Get employee status by employee_number 
    @swagger_auto_schema(manual_parameters=[openapi.Parameter('employeeNumber', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)],  operation_summary="Get Employee Status By Employee Number")
    def get(self, request):
        employee_number = request.GET.get('employeeNumber', None)

        if employee_number:
            try:
                employee = Employee_Status.objects.filter(employee_number=employee_number).first()
                if not employee:
                    response_data = handle_error("Wrong Employee Number", 400)
                    return Response(response_data, 400)
                
            except Exception as error:
                response_data = handle_error(str(error), 500)
                return Response(response_data, 500)
        else:
            response_data = handle_error("Please Enter Valid Employee Number", 400)
            return Response(response_data, 400)
            
        serializer = Employee_Status_Serializer(employee)
        response_data = handle_response(serializer.data, "success", 200, 1)
        return Response(response_data, content_type='application/json')
