from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from subjects.models import Subject
from subjects.serializers import SubjectSerializer
from rest_framework.decorators import api_view


class index(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'subjects/index.html'

    def get(self, request):
        queryset = Subject.objects.all()
        return Response({'subjects': queryset})


class list_all_subjects(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'subjects/subject_list.html'

    def get(self, request):
        queryset = Subject.objects.all()
        return Response({'subject': queryset})


# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def subject_list(request):
    if request.method == 'GET':
        subjects = Subject.objects.all()

        name = request.GET.get('name', None)
        if name is not None:
            subjects = subjects.filter(name__icontains=name)

        subjects_serializer = SubjectSerializer(subjects, many=True)
        return JsonResponse(subjects_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    if request.method == 'POST':
        subject_data = JSONParser().parse(request)
        subject_serializer = SubjectSerializer(data=subject_data)
        if subject_serializer.is_valid():
            subject_serializer.save()
            return JsonResponse(subject_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(subject_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Subject.objects.all().delete()
        return JsonResponse(
            {
                'message':
                '{} Subjects were deleted successfully!'.format(count[0])
            },
            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def subject_detail(request, pk):
    try:
        subject = Subject.objects.get(pk=pk)
    except Subject.DoesNotExist:
        return JsonResponse({'message': 'The subject does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        subject_serializer = SubjectSerializer(subject)
        return JsonResponse(subject_serializer.data)

    elif request.method == 'PUT':
        subject_data = JSONParser().parse(request)
        subject_serializer = SubjectSerializer(subject, data=subject_data)
        if subject_serializer.is_valid():
            subject_serializer.save()
            return JsonResponse(subject_serializer.data)
        return JsonResponse(subject_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        subject.delete()
        return JsonResponse({'message': 'Subject was deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)