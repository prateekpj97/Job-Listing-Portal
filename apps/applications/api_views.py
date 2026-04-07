from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Application
from .serializers import ApplicationSerializer
from apps.jobs.tasks import notify_employer_new_application

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        user = self.request.user
        if user.is_employer():
            return Application.objects.filter(job__posted_by=user).select_related('job', 'applicant')
        return Application.objects.filter(applicant=user).select_related('job')

    def perform_create(self, serializer):
        app = serializer.save(applicant=self.request.user)
        notify_employer_new_application.delay(
            app.job.title, app.job.posted_by.email,
            self.request.user.get_full_name() or self.request.user.username)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.job.posted_by != request.user:
            return Response({'detail': 'Forbidden.'}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)
