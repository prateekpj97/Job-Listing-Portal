from rest_framework import serializers
from .models import Job, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')

class JobSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False)
    posted_by = serializers.StringRelatedField(read_only=True)
    application_count = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ('id', 'title', 'description', 'requirements', 'company', 'location',
                  'salary_min', 'salary_max', 'job_type', 'category', 'category_id',
                  'posted_by', 'deadline', 'is_active', 'created_at', 'application_count')
        read_only_fields = ('posted_by', 'created_at')

    def get_application_count(self, obj):
        return obj.applications.count()

    def create(self, validated_data):
        validated_data['posted_by'] = self.context['request'].user
        return super().create(validated_data)
