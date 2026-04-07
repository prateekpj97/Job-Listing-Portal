from django.contrib import admin
from .models import Job, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'job_type', 'is_active', 'created_at')
    list_filter = ('job_type', 'is_active', 'category')
    search_fields = ('title', 'company', 'location')
    date_hierarchy = 'created_at'
