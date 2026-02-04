from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Path, PathEnrollment
from .serializers import PathSerializer, PathEnrollmentSerializer


class PathListView(generics.ListAPIView):
    """List all available learning paths."""
    queryset = Path.objects.filter(is_active=True)
    serializer_class = PathSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        return {'request': self.request}


class PathDetailView(generics.RetrieveAPIView):
    """Get detailed information about a specific path."""
    queryset = Path.objects.filter(is_active=True)
    serializer_class = PathSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    
    def get_serializer_context(self):
        return {'request': self.request}


@api_view(['POST'])
def enroll_in_path(request, path_id):
    """Enroll user in a learning path."""
    try:
        path = Path.objects.get(id=path_id, is_active=True)
    except Path.DoesNotExist:
        return Response({'error': 'Path not found'}, status=status.HTTP_404_NOT_FOUND)
    
    enrollment, created = PathEnrollment.objects.get_or_create(
        user=request.user,
        path=path
    )
    
    serializer = PathEnrollmentSerializer(enrollment)
    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@api_view(['GET'])
def my_enrollments(request):
    """Get all paths the user is enrolled in."""
    enrollments = PathEnrollment.objects.filter(user=request.user)
    serializer = PathEnrollmentSerializer(enrollments, many=True)
    return Response(serializer.data)
