from rest_framework import serializers
from .models import Lab, LabSession


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = (
            'id', 'name', 'slug', 'description', 'lab_type',
            'docker_image', 'memory_limit', 'cpu_quota', 'timeout_seconds',
            'network_enabled', 'created_at'
        )


class LabSessionSerializer(serializers.ModelSerializer):
    lab_name = serializers.CharField(source='lab.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = LabSession
        fields = (
            'id', 'user', 'username', 'lab', 'lab_name', 'mission',
            'container_id', 'container_name', 'status', 'started_at',
            'stopped_at', 'expires_at', 'command_count', 'error_message',
            'created_at'
        )
        read_only_fields = (
            'container_id', 'container_name', 'status', 'started_at',
            'stopped_at', 'expires_at', 'command_count', 'error_message'
        )
