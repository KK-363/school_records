from django.urls import path
from subjects import views as subjects_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('subjects/', subjects_views.index.as_view(), name='subject'),
    path('api/subjects/', subjects_views.subject_list),
    path('api/subjects/<int:pk>/', subjects_views.subject_detail),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)