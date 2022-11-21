from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from imageapi import views

router = DefaultRouter()
router.register(r'service_plans', views.ServicePlanViewSet, basename='serviceplan')
router.register(r'images', views.ImageViewSet, basename='image')

urlpatterns = [
    path('', include(router.urls)),
    path('image/<str:tmpimg>', views.TempLink.as_view(), name='templink')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
