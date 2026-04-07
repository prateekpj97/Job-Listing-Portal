from rest_framework import serializers
from .models import Application
from apps.jobs.serializers import JobSerializer
from apps.jobs.models import Job

class ApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all(), source='job', write_only=True)
    applicant = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Application
        fields = ('id', 'job', 'job_id', 'applicant', 'cover_letter', 'resume', 'status', 'applied_at')
        read_only_fields = ('applicant', 'status', 'applied_at')

    def create(self, validated_data):
        validated_data['applicant'] = self.context['request'].user
        return super().create(validated_data)
