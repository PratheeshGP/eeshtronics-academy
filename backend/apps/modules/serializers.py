from rest_framework import serializers
from .models import Module, ModuleUnlock


class ModuleSerializer(serializers.ModelSerializer):
    path_title = serializers.CharField(source='path.title', read_only=True)
    mission_count = serializers.SerializerMethodField()
    is_unlocked = serializers.SerializerMethodField()
    
    class Meta:
        model = Module
        fields = (
            'id', 'path', 'path_title', 'title', 'slug', 'description',
            'order', 'ether_cost', 'completion_xp', 'completion_ether',
            'learning_objectives', 'estimated_hours', 'mission_count',
            'is_unlocked', 'is_locked_by_default'
        )
    
    def get_mission_count(self, obj):
        return obj.get_mission_count()
    
    def get_is_unlocked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if not obj.is_locked_by_default:
                return True
            return ModuleUnlock.objects.filter(user=request.user, module=obj).exists()
        return False


class ModuleUnlockSerializer(serializers.ModelSerializer):
    module_title = serializers.CharField(source='module.title', read_only=True)
    
    class Meta:
        model = ModuleUnlock
        fields = ('id', 'module', 'module_title', 'progress_percentage', 'completed_at', 'created_at')
        read_only_fields = ('progress_percentage', 'completed_at')
