from rest_framework.views import APIView
from rest_framework.response import Response
from error_handling.error_handler import handle_error
from .models import Task_Card_Log
from response_handling.response_handler import handle_response
from .serializer import Task_Card_Log_Post_Serializer, Task_Card_Log_Patch_Serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from django.utils import timezone

# Create your views here.

class taskCardTracker(APIView):
    #Add task card
    @swagger_auto_schema(request_body=Task_Card_Log_Post_Serializer, operation_summary="Create/Book A New Task Card")
    def post(self, request):
        request_body = request.data
        request_body['start_time'] = timezone.now().time().strftime('%H:%M:%S')
        task_card_exist = Task_Card_Log.objects.filter(task_card_barcode=request_body['task_card_barcode']).exists()
        
        if task_card_exist:
            response_data = handle_error("Task Card Already Exists", 403)
            return Response(response_data, 403)

        barcode_length = len(request_body['task_card_barcode'])

        if barcode_length not in [7,13]:
            response_data = handle_error("Task Card Barcode Is Invalid", 400)
            return Response(response_data, 400)
        if barcode_length == 13:
            request_body['nrc'] = "no"
            request_body['task_card_number'] = request_body['task_card_barcode'][6:]
        else:
            request_body['task_card_number'] = request_body['task_card_barcode']
            request_body['nrc'] = "yes"

        serializers = Task_Card_Log_Post_Serializer(data = request_body)

        #validate input data
        if serializers.is_valid():

            try:
                serializers.save()
            except Exception as error:
                response_data = handle_error(str(error), 500)
                return Response(response_data, 500)
            response_data = handle_response(serializers.data, "success", 200, 1)
            return Response(response_data, 200)
        else:
            err = list(serializers.errors)
            response_data = handle_error(f"Fields Missing/Invalid : {err}", 400)
            return Response(response_data, 400)

    #combine multiple filter
    def build_filter(self, request):
        filters = Q()
        employee_number = request.GET.get('employeeNumber', None)
        type_of_data = request.GET.get('typeOfData', None)

        if employee_number:
            #handle request of task card booking
            filters &= Q(employee_number=employee_number)
            if type_of_data != "All":
                filters &= Q(end_date=None)

        else:
            #handle request of task card tracker
            # Retrieve query parameters
            work_order = request.GET.get('workOrder', None)
            task_card_number = request.GET.get('taskCardNumber', None)
            location = request.GET.get('location', None)
            time_phase = request.GET.get('timePhase', None)
            production_phase = request.GET.get('productionPhase', None)
            user = request.GET.get('user', None)
            
            # Build filter conditions dynamically
            if work_order:
                filters &= Q(work_order=work_order)
            if task_card_number:
                filters &= Q(task_card_number=task_card_number)
            if location:
                filters &= Q(location=location)
            if time_phase:
                filters &= Q(time_phase=time_phase)
            if production_phase:
                filters &= Q(production_phase=production_phase)
            if user:
                filters &= Q(employee_number=user)
        
        return filters

    #Get all task cards
    @swagger_auto_schema(manual_parameters=[openapi.Parameter('workOrder', openapi.IN_QUERY, type=openapi.TYPE_STRING),
                                            openapi.Parameter('taskCardNumber', openapi.IN_QUERY, type=openapi.TYPE_STRING),
                                            openapi.Parameter('location', openapi.IN_QUERY, type=openapi.TYPE_STRING),
                                            openapi.Parameter('timePhase', openapi.IN_QUERY, type=openapi.TYPE_STRING),
                                            openapi.Parameter('productionPhase', openapi.IN_QUERY, type=openapi.TYPE_STRING),
                                            openapi.Parameter('user', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
                                            openapi.Parameter('limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
                                            openapi.Parameter('skip', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
                                            openapi.Parameter('employeeNumber', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
                                            openapi.Parameter('typeOfData', openapi.IN_QUERY, type=openapi.TYPE_STRING)
                                            ], operation_summary="Get Task Cards With Filter")
    def get(self, request):
        try:
            task_card_list = Task_Card_Log.objects.all().order_by('-id')
            task_card_list_length = len(task_card_list)
        except Exception as error:
            response_data = handle_error(str(error), 500)
            return Response(response_data, 500)
        
        limit = int(request.GET.get('limit', 100))
        skip = int(request.GET.get('skip', 0))

        filters = self.build_filter(request)

        # Apply filters to the task_card_list if any filter conditions are present
        if filters:
            task_card_list = task_card_list.filter(filters)
            task_card_list_length = len(task_card_list)
            
        task_card_list = task_card_list[skip:skip+limit]
        
        if len(task_card_list) < 1:
            response_data = handle_error("Data Not Found", 404)
            return Response(response_data, 404)

        serializer = Task_Card_Log_Post_Serializer(task_card_list, many=True)
        response_data = handle_response(serializer.data, "success", 200, task_card_list_length)
        return Response(response_data, 200)


    #Delete task card
    @swagger_auto_schema(manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),], operation_summary="Delete A Specific Task Card")
    def delete(self, request):
        id = request.GET.get('id', None)
        if not id:
            response_data = handle_error("Id Is Required", 400)
            return Response(response_data, 400)
        
        try:
            task_card = Task_Card_Log.objects.get(pk=id)
            task_card.delete()
        except Exception as error:
            response_data = handle_error(str(error), 500)
            return Response(response_data, 500)

        response_data = handle_response("Data Deleted", "success", 200, 1)
        return Response(response_data, 200)


    def update_data(self, request_body):
        if 'id' not in request_body:
            response_data = {"error":"Id Is Required", "status_code":400}
            return response_data
        if "status" in request_body:
            if request_body['status'] in ['closed', 'canceled']:
                request_body['end_date'] = timezone.now().date().strftime('%Y-%m-%d')
                request_body['end_time'] = timezone.now().time().strftime('%H:%M:%S')

        try:
            task_card = Task_Card_Log.objects.get(pk=request_body['id'])
        except Exception as error:
            response_data = {"error":str(error), "status_code":500}
            return response_data

        serializers = Task_Card_Log_Patch_Serializer(instance=task_card, data=request_body, partial=True)

        #validate input data
        if serializers.is_valid():
            try:
                serializers.save()
            except Exception as error:
                response_data = {"error":str(error), "status_code":500}
                return response_data
            response_data = {"result":"Task Card Updated", "status_code":200}
            return response_data

        else:
            err = list(serializers.errors)
            response_data = {"error":f"Fields Missing/Invalid : {err}", "status_code": 400}
            return response_data


    #Update task card
    @swagger_auto_schema(request_body=Task_Card_Log_Patch_Serializer, operation_summary="Update Fields In Task Card")
    def patch(self, request):
        request_body = request.data
        
        if "task_card_list" in request_body:
            task_card_list = request_body['task_card_list']
            data_length = len(task_card_list)
            #iterate each task card from list
            for single_task_card in task_card_list: 
                response_data = self.update_data(single_task_card)
                if "error" in response_data:
                    response_data = handle_error(response_data['error'], response_data['status_code'])
                    return Response(response_data, response_data['error']['error_code'])
        else:
            data_length = 1
            response_data = self.update_data(request_body)
            if "error" in response_data:
                response_data = handle_error(response_data['error'], response_data['status_code'])
                return Response(response_data, response_data['error']['error_code'])
    
        response_data = handle_response(response_data, "success", 200, data_length)
        return Response(response_data, 200)

