from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_applications, name='my_applications'),
    path('apply/<int:job_pk>/', views.apply, name='apply'),
    path('job/<int:job_pk>/', views.job_applications, name='job_applications'),
    path('<int:pk>/status/', views.update_status, name='update_status'),
]
