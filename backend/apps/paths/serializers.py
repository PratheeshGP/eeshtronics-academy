from rest_framework import serializers
from .models import Path, PathEnrollment


class PathSerializer(serializers.ModelSerializer):
    module_count = serializers.SerializerMethodField()
    total_missions = serializers.SerializerMethodField()
    is_enrolled = serializers.SerializerMethodField()
    
    class Meta:
        model = Path
        fields = (
            'id', 'title', 'slug', 'description', 'difficulty',
            'estimated_hours', 'completion_xp', 'completion_ether',
            'thumbnail', 'is_featured', 'module_count', 'total_missions',
            'is_enrolled', 'created_at'
        )
    
    def get_module_count(self, obj):
        return obj.get_module_count()
    
    def get_total_missions(self, obj):
        return obj.get_total_missions()
    
    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PathEnrollment.objects.filter(user=request.user, path=obj).exists()
        return False


class PathEnrollmentSerializer(serializers.ModelSerializer):
    path_title = serializers.CharField(source='path.title', read_only=True)
    
    class Meta:
        model = PathEnrollment
        fields = ('id', 'path', 'path_title', 'progress_percentage', 'completed_at', 'created_at')
        read_only_fields = ('progress_percentage', 'completed_at')
