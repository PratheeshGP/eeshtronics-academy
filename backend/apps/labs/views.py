from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Lab, LabSession
from .serializers import LabSerializer, LabSessionSerializer
from apps.sandbox.tasks import launch_lab_container_task, terminate_lab_container_task


class LabListView(generics.ListAPIView):
    """List all available labs."""
    queryset = Lab.objects.all()
    serializer_class = LabSerializer
    permission_classes = [IsAuthenticated]


class LabDetailView(generics.RetrieveAPIView):
    """Get detailed lab information."""
    queryset = Lab.objects.all()
    serializer_class = LabSerializer
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
def start_lab(request):
    """
    Start a new lab session.
    POST /api/labs/start
    Body: {"lab_id": 1, "mission_id": 5 (optional)}
    """
    lab_id = request.data.get('lab_id')
    mission_id = request.data.get('mission_id')
    
    if not lab_id:
        return Response({'error': 'lab_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        lab = Lab.objects.get(id=lab_id)
    except Lab.DoesNotExist:
        return Response({'error': 'Lab not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if user already has an active session for this lab
    active_session = LabSession.objects.filter(
        user=request.user,
        lab=lab,
        status__in=['PENDING', 'STARTING', 'RUNNING']
    ).first()
    
    if active_session:
        return Response(
            {'error': 'You already have an active session for this lab', 'session': LabSessionSerializer(active_session).data},
            status=status.HTTP_409_CONFLICT
        )
    
    # Create new session
    session = LabSession.objects.create(
        user=request.user,
        lab=lab,
        mission_id=mission_id,
        status='PENDING'
    )
    
    # Launch container asynchronously
    launch_lab_container_task.delay(session.id)
    
    return Response(LabSessionSerializer(session).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def stop_lab(request, session_id):
    """
    Stop a running lab session.
    POST /api/labs/<session_id>/stop
    """
    try:
        session = LabSession.objects.get(id=session_id, user=request.user)
    except LabSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if session.status not in ['RUNNING', 'STARTING']:
        return Response({'error': 'Session is not active'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Terminate container asynchronously
    terminate_lab_container_task.delay(session.id)
    
    return Response({'message': 'Lab session is stopping'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def lab_status(request, session_id):
    """
    Get status of a lab session.
    GET /api/labs/<session_id>/status
    """
    try:
        session = LabSession.objects.get(id=session_id, user=request.user)
    except LabSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(LabSessionSerializer(session).data)


@api_view(['GET'])
def my_sessions(request):
    """Get all lab sessions for the current user."""
    sessions = LabSession.objects.filter(user=request.user)
    serializer = LabSessionSerializer(sessions, many=True)
    return Response(serializer.data)
