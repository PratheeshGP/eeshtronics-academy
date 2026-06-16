from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import MissionProgress, UserStreak, UserAchievement, RequirementTracker
from .serializers import (
    MissionProgressSerializer, UserStreakSerializer, 
    UserAchievementSerializer, RequirementTrackerSerializer
)


@api_view(['POST'])
def update_mission_progress(request):
    """
    Update progress for a mission.
    POST /api/progress/update
    Body: {"mission_id": 1, "status": "IN_PROGRESS", "progress_percentage": 50}
    """
    mission_id = request.data.get('mission_id')
    new_status = request.data.get('status')
    progress_pct = request.data.get('progress_percentage', 0)
    
    if not mission_id:
        return Response({'error': 'mission_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    progress, created = MissionProgress.objects.get_or_create(
        user=request.user,
        mission_id=mission_id,
        defaults={'started_at': timezone.now()}
    )
    
    if new_status:
        progress.status = new_status
    if progress_pct:
        progress.progress_percentage = progress_pct
    
    progress.attempt_count += 1
    progress.save()
    
    # Update streak
    streak, _ = UserStreak.objects.get_or_create(user=request.user)
    streak.update_streak()
    
    serializer = MissionProgressSerializer(progress)
    return Response(serializer.data)


@api_view(['POST'])
def complete_mission(request, mission_id):
    """
    Mark a mission as completed.
    POST /api/progress/mission/<id>/complete
    Body: {"score": 95}
    """
    score = request.data.get('score', 100)
    
    try:
        progress = MissionProgress.objects.get(user=request.user, mission_id=mission_id)
    except MissionProgress.DoesNotExist:
        progress = MissionProgress.objects.create(
            user=request.user,
            mission_id=mission_id,
            started_at=timezone.now()
        )
    
    progress.mark_complete(score)
    
    # Update streak
    streak, _ = UserStreak.objects.get_or_create(user=request.user)
    streak.update_streak()
    
    serializer = MissionProgressSerializer(progress)
    return Response(serializer.data)


@api_view(['GET'])
def user_progress_summary(request):
    """
    Get comprehensive progress summary for user.
    GET /api/progress/user
    """
    # Mission progress
    missions = MissionProgress.objects.filter(user=request.user)
    
    # Streak
    streak, _ = UserStreak.objects.get_or_create(user=request.user)
    
    # Achievements
    achievements = UserAchievement.objects.filter(user=request.user)
    
    summary = {
        'user': {
            'username': request.user.username,
            'level': request.user.level,
            'xp_points': request.user.xp_points,
            'ether_balance': float(request.user.ether_balance),
        },
        'missions': {
            'total': missions.count(),
            'completed': missions.filter(status='COMPLETED').count(),
            'in_progress': missions.filter(status='IN_PROGRESS').count(),
            'recent': MissionProgressSerializer(missions[:5], many=True).data,
        },
        'streak': UserStreakSerializer(streak).data,
        'achievements': {
            'total_earned': achievements.count(),
            'recent': UserAchievementSerializer(achievements[:5], many=True).data,
        }
    }
    
    return Response(summary)


@api_view(['GET'])
def my_achievements(request):
    """Get all achievements earned by the user."""
    achievements = UserAchievement.objects.filter(user=request.user)
    serializer = UserAchievementSerializer(achievements, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def requirements_list_create(request):
    """
    List user requirements (or all if admin) or create a new one.
    """
    if request.method == 'GET':
        if request.user.is_staff:
            requirements = RequirementTracker.objects.all()
        else:
            requirements = RequirementTracker.objects.filter(user=request.user)
        serializer = RequirementTrackerSerializer(requirements, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        serializer = RequirementTrackerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def requirement_detail_update(request, pk):
    """
    Update (admin) or delete (user/admin) a requirement upload.
    """
    try:
        requirement = RequirementTracker.objects.get(pk=pk)
    except RequirementTracker.DoesNotExist:
        return Response({'error': 'Requirement not found'}, status=status.HTTP_404_NOT_FOUND)
        
    if requirement.user != request.user and not request.user.is_staff:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
    if request.method == 'DELETE':
        requirement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    elif request.method == 'PATCH':
        serializer = RequirementTrackerSerializer(requirement, data=request.data, partial=True)
        if serializer.is_valid():
            new_status = request.data.get('status')
            if new_status == 'COMPLETED' and not requirement.completed_at:
                # Set completed_at timestamp
                serializer.save(completed_at=timezone.now())
            else:
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
