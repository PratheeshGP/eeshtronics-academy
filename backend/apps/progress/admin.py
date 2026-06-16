from django.contrib import admin
from .models import RequirementTracker

@admin.register(RequirementTracker)
class RequirementTrackerAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'created_at', 'completed_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'user__username', 'description')
    readonly_fields = ('created_at', 'updated_at')
