"""
Celery tasks for sandbox container management.
"""
from celery import shared_task
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def launch_lab_container_task(self, session_id):
    """
    Asynchronously launch a Docker container for a lab session.
    """
    from apps.labs.models import LabSession
    from .docker_executor import DockerSandboxExecutor
    
    try:
        session = LabSession.objects.get(id=session_id)
        session.status = 'STARTING'
        session.save()
        
        executor = DockerSandboxExecutor()
        container = executor.create_container(session.lab, session)
        
        if container:
            logger.info(f"Successfully launched container for session {session_id}")
            return {'status': 'success', 'container_id': container.id}
        else:
            logger.error(f"Failed to launch container for session {session_id}")
            return {'status': 'error', 'message': 'Container creation failed'}
            
    except LabSession.DoesNotExist:
        logger.error(f"LabSession {session_id} not found")
        return {'status': 'error', 'message': 'Session not found'}
        
    except Exception as e:
        logger.error(f"Error in launch_lab_container_task: {e}")
        # Retry on failure
        raise self.retry(exc=e, countdown=5)


@shared_task
def terminate_lab_container_task(session_id):
    """
    Asynchronously stop and remove a lab container.
    """
    from apps.labs.models import LabSession
    from .docker_executor import DockerSandboxExecutor
    
    try:
        session = LabSession.objects.get(id=session_id)
        executor = DockerSandboxExecutor()
        executor.stop_container(session)
        
        logger.info(f"Successfully terminated container for session {session_id}")
        return {'status': 'success'}
        
    except LabSession.DoesNotExist:
        logger.error(f"LabSession {session_id} not found")
        return {'status': 'error', 'message': 'Session not found'}
        
    except Exception as e:
        logger.error(f"Error in terminate_lab_container_task: {e}")
        return {'status': 'error', 'message': str(e)}


@shared_task
def cleanup_expired_containers_task():
    """
    Periodic task to cleanup expired containers.
    Should be run via Celery Beat every 5 minutes.
    """
    from .docker_executor import DockerSandboxExecutor
    
    try:
        executor = DockerSandboxExecutor()
        count = executor.cleanup_expired_containers()
        
        logger.info(f"Cleanup task completed. Removed {count} expired containers")
        return {'status': 'success', 'cleaned_count': count}
        
    except Exception as e:
        logger.error(f"Error in cleanup_expired_containers_task: {e}")
        return {'status': 'error', 'message': str(e)}
