from django.urls import path
from events import views as events_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('events/', events_views.index.as_view(), name='event'),
    path('api/events/', events_views.event_list),
    path('api/events/<int:pk>/', events_views.event_detail),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)