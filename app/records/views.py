from datetime import date
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from students.models import Student
from records.models import Record
from records.serializers import RecordSerializer
from rest_framework.decorators import api_view


class index(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'records/index.html'

    def get(self, request):
        queryset = Record.objects.all()
        queryset2 = Student.objects.all()        

        return Response({'records': queryset})


class list_all_records(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'records/record_list.html'

    def get(self, request):
        queryset = Record.objects.all()
        return Response({'record': queryset})


# Create your views here.
@api_view(['GET', 'POST'])
def record_list(request):
    if request.method == 'GET':
        records = Record.objects.all()

        date = request.GET.get('date', None)
        if date is not None:
            records = records.filter(date__icontains=date)

        records_serializer = RecordSerializer(records, many=True)
        return JsonResponse(records_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    if request.method == 'POST':
        record_data = JSONParser().parse(request)
        record_serializer = RecordSerializer(data=record_data)
        if record_serializer.is_valid():
            record_serializer.save()
            return JsonResponse(record_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(record_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def record_detail(request, pk):
    try:
        record = Record.objects.get(pk=pk)
    except Record.DoesNotExist:
        return JsonResponse({'message': 'The record does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        record_serializer = RecordSerializer(record)
        return JsonResponse(record_serializer.data)

    elif request.method == 'PUT':
        record_data = JSONParser().parse(request)
        record_serializer = RecordSerializer(record, data=record_data)
        if record_serializer.is_valid():
            record_serializer.save()
            return JsonResponse(record_serializer.data)
        return JsonResponse(record_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        record.delete()
        return JsonResponse({'message': 'Record was deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)