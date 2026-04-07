from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ApplicationViewSet

router = DefaultRouter()
router.register(r'', ApplicationViewSet, basename='api-application')

urlpatterns = [path('', include(router.urls))]
