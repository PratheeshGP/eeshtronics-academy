from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Mission, Artifact
from .serializers import MissionSerializer, ArtifactSerializer


class MissionListView(generics.ListAPIView):
    """List missions, optionally filtered by module."""
    serializer_class = MissionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Mission.objects.all()
        module_id = self.request.query_params.get('module', None)
        if module_id:
            queryset = queryset.filter(module_id=module_id)
        return queryset
    
    def get_serializer_context(self):
        return {'request': self.request}


class MissionDetailView(generics.RetrieveAPIView):
    """Get detailed mission information."""
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    
    def get_serializer_context(self):
        return {'request': self.request}


class ArtifactCreateView(generics.CreateAPIView):
    """Submit an artifact for a mission."""
    serializer_class = ArtifactSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        artifact = serializer.save(user=self.request.user)
        
        # Trigger async validation if enabled
        if artifact.mission.auto_validate:
            from apps.progress.tasks import validate_artifact_task
            validate_artifact_task.delay(artifact.id)


class ArtifactListView(generics.ListAPIView):
    """List user's submitted artifacts."""
    serializer_class = ArtifactSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Artifact.objects.filter(user=self.request.user)
