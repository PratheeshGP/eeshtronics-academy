from rest_framework import serializers
from .models import Mission, Exercise, Artifact


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('id', 'title', 'description', 'order', 'xp_reward')


class MissionSerializer(serializers.ModelSerializer):
    module_title = serializers.CharField(source='module.title', read_only=True)
    exercises = ExerciseSerializer(many=True, read_only=True)
    user_progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Mission
        fields = (
            'id', 'module', 'module_title', 'title', 'slug', 'description',
            'difficulty', 'mission_brief', 'hints', 'required_artifact_type',
            'xp_reward', 'ether_reward', 'estimated_minutes', 'requires_lab',
            'associated_lab', 'exercises', 'user_progress'
        )
    
    def get_user_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from apps.progress.models import MissionProgress
            try:
                progress = MissionProgress.objects.get(user=request.user, mission=obj)
                return {
                    'status': progress.status,
                    'progress_percentage': float(progress.progress_percentage),
                    'score': progress.score
                }
            except MissionProgress.DoesNotExist:
                return None
        return None


class ArtifactSerializer(serializers.ModelSerializer):
    mission_title = serializers.CharField(source='mission.title', read_only=True)
    
    class Meta:
        model = Artifact
        fields = (
            'id', 'mission', 'mission_title', 'submission_type',
            'content', 'file', 'is_validated', 'validation_result',
            'score', 'feedback', 'created_at'
        )
        read_only_fields = ('is_validated', 'validation_result', 'score', 'feedback')
