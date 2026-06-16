"""
Celery tasks for progress tracking and validation.
"""
from celery import shared_task
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


@shared_task
def validate_artifact_task(artifact_id):
    """
    Asynchronously validate a submitted artifact.
    """
    from apps.missions.models import Artifact
    from apps.progress.models import MissionProgress
    
    try:
        artifact = Artifact.objects.get(id=artifact_id)
        mission = artifact.mission
        
        # TODO: Implement actual validation logic based on mission.validation_script
        # For now, simple mock validation
        artifact.is_validated = True
        artifact.score = 85
        artifact.validation_result = {
            'status': 'PASS',
            'message': 'Artifact validated successfully',
            'timestamp': str(timezone.now())
        }
        artifact.save()
        
        # Update mission progress
        progress, _ = MissionProgress.objects.get_or_create(
            user=artifact.user,
            mission=mission
        )
        
        if artifact.score >= 70:
            progress.mark_complete(artifact.score)
        
        logger.info(f"Artifact {artifact_id} validated successfully")
        return {'status': 'success', 'score': artifact.score}
        
    except Artifact.DoesNotExist:
        logger.error(f"Artifact {artifact_id} not found")
        return {'status': 'error', 'message': 'Artifact not found'}
        
    except Exception as e:
        logger.error(f"Error validating artifact: {e}")
        return {'status': 'error', 'message': str(e)}
