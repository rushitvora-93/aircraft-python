from rest_framework.views import APIView
from rest_framework.response import Response
from error_handling.error_handler import handle_error
from .models import Material_Movement_Log
from response_handling.response_handler import handle_response
from .serializer import Material_Movement_Log_Post_Serializer, Material_Movement_Log_Patch_Serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q


class partNumberTracker(APIView):
    #Add Material
    @swagger_auto_schema(request_body=Material_Movement_Log_Post_Serializer, operation_summary="Add Material/Part")
    def post(self, request):
        request_body = request.data
        serializers = Material_Movement_Log_Post_Serializer(data = request_body)

        #validate input data
        if serializers.is_valid():
            material_exist = Material_Movement_Log.objects.filter(requirement_number=request_body['requirement_number']).exists()
            if material_exist:
                response_data = handle_error("Material Already Exists", 400)
                return Response(response_data, 400)

            if len(request_body['requirement_number']) != 6:
                response_data = handle_error("Requirement Number Is Invalid", 400)
                return Response(response_data, 400)

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
            
    #Get all Materials
    @swagger_auto_schema(manual_parameters=[openapi.Parameter('partNumber', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
                                            openapi.Parameter('requirementNumber', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
                                            openapi.Parameter('limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
                                            openapi.Parameter('skip', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
                                            openapi.Parameter('workOrder', openapi.IN_QUERY, type=openapi.TYPE_STRING)
                                            ], operation_summary="Get Materials/Parts List With Filter")
    def get(self, request):
        try:
            material_list = Material_Movement_Log.objects.all().order_by('-id')
            material_list_length = len(material_list)
        except Exception as error:
            response_data = handle_error(str(error), 500)
            return Response(response_data, 500)
        
        limit = int(request.GET.get('limit', 100))
        skip = int(request.GET.get('skip', 0))

        filters = Q()
        part_number = request.GET.get('partNumber', None)
        requirement_number = request.GET.get('requirementNumber', None)
        work_order = request.GET.get('workOrder', None)

        # Build filter conditions dynamically
        if part_number:
            filters &= Q(part_number=part_number)
        if requirement_number:
            filters &= Q(requirement_number=requirement_number)
        if work_order:
            filters &= Q(work_order=work_order)

        # Apply filters to the task_card_list if any filter conditions are present
        if filters:
            material_list = material_list.filter(filters)
            material_list_length = len(material_list)

        material_list = material_list[skip:skip+limit]
            
        if len(material_list) < 1:
            response_data = handle_error("Data Not Found", 404)
            return Response(response_data, 404)

        serializer = Material_Movement_Log_Post_Serializer(material_list, many=True)
        response_data = handle_response(serializer.data, "success", 200, material_list_length)
        return Response(response_data, 200)


    #Delete Material
    @swagger_auto_schema(manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)], operation_summary="Delete A Specific Part/Material")
    def delete(self, request):
        id = request.GET.get('id', None)
        if not id:
            response_data = handle_error("Id Is Required", 400)
            return Response(response_data, 400)
        
        try:
            material = Material_Movement_Log.objects.get(pk=id)
            material.delete()
        except Exception as error:
            response_data = handle_error(str(error), 500)
            return Response(response_data, 500)

        response_data = handle_response("Data Deleted", "success", 200, 1)
        return Response(response_data, 200)


    #Update Material
    @swagger_auto_schema(request_body=Material_Movement_Log_Patch_Serializer, operation_summary="Update Fields In Part/Material")
    def patch(self, request):
        request_body = request.data
        if 'id' not in request_body:
            response_data = handle_error("Id Is Required", 400)
            return Response(response_data, 400)
        
        try:
            material = Material_Movement_Log.objects.get(pk=request_body['id'])
        except Exception as error:
            response_data = handle_error(str(error), 500)
            return Response(response_data, 500)

        serializers = Material_Movement_Log_Patch_Serializer(instance=material, data=request_body, partial=True)

        #validate input data
        if serializers.is_valid():
            try:
                serializers.save()
            except Exception as error:
                response_data = handle_error(str(error), 500)
                return Response(response_data, 500)

            response_data = handle_response("Material Data Updated", "success", 200, 1)
            return Response(response_data, 200)

        else:
            err = list(serializers.errors)
            response_data = handle_error(f"Fields Missing/Invalid : {err}", 400)
            return Response(response_data, 400)
