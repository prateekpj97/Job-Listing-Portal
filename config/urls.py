from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('', include('apps.jobs.urls')),
    path('applications/', include('apps.applications.urls')),
    path('api/', include('apps.jobs.api_urls')),
    path('api/applications/', include('apps.applications.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
