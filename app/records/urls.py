from django.urls import path
from records import views as records_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('records/', records_views.index.as_view(), name='record'),
    path('api/records/', records_views.record_list),
    path('api/records/<int:pk>/', records_views.record_detail),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)