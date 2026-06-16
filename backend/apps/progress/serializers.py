from rest_framework import serializers
from .models import MissionProgress, UserStreak, Achievement, UserAchievement, RequirementTracker


class MissionProgressSerializer(serializers.ModelSerializer):
    mission_title = serializers.CharField(source='mission.title', read_only=True)
    
    class Meta:
        model = MissionProgress
        fields = (
            'id', 'mission', 'mission_title', 'status', 'progress_percentage',
            'score', 'started_at', 'completed_at', 'time_spent_seconds',
            'attempt_count', 'created_at', 'updated_at'
        )
        read_only_fields = ('started_at', 'completed_at', 'attempt_count')


class UserStreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStreak
        fields = ('current_streak', 'longest_streak', 'last_activity_date')


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = (
            'id', 'name', 'description', 'category', 'requirement_description',
            'requirement_value', 'xp_reward', 'ether_reward', 'icon'
        )


class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer(read_only=True)
    
    class Meta:
        model = UserAchievement
        fields = ('id', 'achievement', 'earned_at')


class RequirementTrackerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    file_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = RequirementTracker
        fields = (
            'id', 'user', 'username', 'title', 'description', 'file', 'file_name',
            'status', 'admin_notes', 'completed_at', 'created_at', 'updated_at'
        )
        read_only_fields = ('user', 'completed_at', 'created_at', 'updated_at')
        
    def get_file_name(self, obj):
        if obj.file:
            return obj.file.name.split('/')[-1]
        return None
