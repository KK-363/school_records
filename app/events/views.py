from datetime import date
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import Event
from events.serializers import EventSerializer
from rest_framework.decorators import api_view


class index(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'events/index.html'

    def get(self, request):
        queryset = Event.objects.all()
        queryset2 = Event.objects.all()        

        return Response({'events': queryset})


class list_all_events(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'events/event_list.html'

    def get(self, request):
        queryset = Event.objects.all()
        return Response({'event': queryset})


# Create your views here.
@api_view(['GET', 'POST'])
def event_list(request):
    if request.method == 'GET':
        events = Event.objects.all()

        name = request.GET.get('name', None)
        if name is not None:
            events = events.filter(name__icontains=name)

        events_serializer = EventSerializer(events, many=True)
        return JsonResponse(events_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    if request.method == 'POST':
        event_data = JSONParser().parse(request)
        event_serializer = EventSerializer(data=event_data)
        if event_serializer.is_valid():
            event_serializer.save()
            return JsonResponse(event_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(event_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def event_detail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return JsonResponse({'message': 'The event does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        event_serializer = EventSerializer(event)
        return JsonResponse(event_serializer.data)

    elif request.method == 'PUT':
        event_data = JSONParser().parse(request)
        event_serializer = EventSerializer(event, data=event_data)
        if event_serializer.is_valid():
            event_serializer.save()
            return JsonResponse(event_serializer.data)
        return JsonResponse(event_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        event.delete()
        return JsonResponse({'message': 'Event was deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)

