from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import JobViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='api-job')
router.register(r'categories', CategoryViewSet, basename='api-category')

urlpatterns = [path('', include(router.urls))]
