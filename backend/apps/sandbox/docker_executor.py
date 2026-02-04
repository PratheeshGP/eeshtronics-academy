"""
Docker sandbox executor for lab containers.
Handles container lifecycle with security isolation.
"""
import docker
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


class DockerSandboxExecutor:
    """
    Manages Docker containers for lab sessions with security constraints.
    """
    
    def __init__(self):
        """Initialize Docker client."""
        try:
            self.client = docker.from_env()
            logger.info("Docker client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            raise
    
    def create_container(self, lab, session):
        """
        Create and start a new container for a lab session.
        
        Args:
            lab: Lab instance with Docker configuration
            session: LabSession instance to associate with container
        
        Returns:
            Container object if successful, None otherwise
        """
        try:
            container_name = f"lab_{session.id}_{session.user.username}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Build resource limits
            host_config = {
                'mem_limit': lab.memory_limit,
                'cpu_quota': lab.cpu_quota,
                'cpu_period': 100000,  # 100ms
                'security_opt': ['no-new-privileges'],  # Prevent privilege escalation
            }
            
            # Network configuration
            if not lab.network_enabled:
                host_config['network_mode'] = 'none'  # Disable network
            
            # Create container (NOT privileged)
            container = self.client.containers.run(
                image=lab.docker_image,
                name=container_name,
                detach=True,
                stdin_open=True,
                tty=True,
                environment=lab.environment_variables,
                command=lab.startup_command if lab.startup_command else '/bin/bash',
                **host_config,
                remove=False,  # Don't auto-remove; we'll clean up manually
            )
            
            logger.info(f"Container {container_name} created successfully")
            
            # Update session
            session.container_id = container.id
            session.container_name = container_name
            session.status = 'RUNNING'
            session.started_at = timezone.now()
            session.expires_at = timezone.now() + timedelta(seconds=lab.timeout_seconds)
            session.save()
            
            return container
            
        except docker.errors.ImageNotFound:
            logger.error(f"Docker image not found: {lab.docker_image}")
            session.status = 'ERROR'
            session.error_message = f"Docker image not found: {lab.docker_image}"
            session.save()
            return None
            
        except docker.errors.APIError as e:
            logger.error(f"Docker API error: {e}")
            session.status = 'ERROR'
            session.error_message = str(e)
            session.save()
            return None
            
        except Exception as e:
            logger.error(f"Unexpected error creating container: {e}")
            session.status = 'ERROR'
            session.error_message = str(e)
            session.save()
            return None
    
    def execute_command(self, container_id, command, session=None):
        """
        Execute a command inside a running container.
        
        Args:
            container_id: Docker container ID
            command: Command string to execute
            session: LabSession for tracking (optional)
        
        Returns:
            Dict with 'output' and 'error' keys
        """
        try:
            container = self.client.containers.get(container_id)
            
            # Security: Filter dangerous commands
            if self._is_dangerous_command(command):
                logger.warning(f"Blocked dangerous command: {command}")
                return {
                    'output': '',
                    'error': 'Command blocked for security reasons'
                }
            
            # Execute command
            result = container.exec_run(command, tty=True)
            
            # Update command count
            if session:
                session.command_count += 1
                session.save()
            
            return {
                'output': result.output.decode('utf-8', errors='replace'),
                'exit_code': result.exit_code,
                'error': '' if result.exit_code == 0 else f"Exit code: {result.exit_code}"
            }
            
        except docker.errors.NotFound:
            return {'output': '', 'error': 'Container not found'}
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return {'output': '', 'error': str(e)}
    
    def stop_container(self, session):
        """
        Stop and remove a container.
        
        Args:
            session: LabSession instance
        """
        try:
            if not session.container_id:
                logger.warning(f"No container ID for session {session.id}")
                return
            
            container = self.client.containers.get(session.container_id)
            container.stop(timeout=10)
            container.remove()
            
            logger.info(f"Container {session.container_name} stopped and removed")
            
            # Update session
            session.status = 'STOPPED'
            session.stopped_at = timezone.now()
            session.save()
            
        except docker.errors.NotFound:
            logger.warning(f"Container {session.container_id} not found")
            session.status = 'STOPPED'
            session.save()
            
        except Exception as e:
            logger.error(f"Error stopping container: {e}")
            session.status = 'ERROR'
            session.error_message = str(e)
            session.save()
    
    def cleanup_expired_containers(self):
        """
        Find and terminate all expired lab sessions.
        Run periodically via Celery beat.
        """
        from apps.labs.models import LabSession
        
        expired_sessions = LabSession.objects.filter(
            status='RUNNING',
            expires_at__lte=timezone.now()
        )
        
        count = 0
        for session in expired_sessions:
            logger.info(f"Cleaning up expired session {session.id}")
            self.stop_container(session)
            session.status = 'EXPIRED'
            session.save()
            count += 1
        
        logger.info(f"Cleaned up {count} expired containers")
        return count
    
    def get_container_stats(self, container_id):
        """
        Get resource usage statistics for a container.
        
        Returns:
            Dict with CPU and memory usage
        """
        try:
            container = self.client.containers.get(container_id)
            stats = container.stats(stream=False)
            
            # Calculate CPU percentage
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                       stats['precpu_stats']['cpu_usage']['total_usage']
            system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                          stats['precpu_stats']['system_cpu_usage']
            cpu_percent = (cpu_delta / system_delta) * 100.0 if system_delta > 0 else 0.0
            
            # Memory usage
            memory_usage = stats['memory_stats'].get('usage', 0)
            memory_limit = stats['memory_stats'].get('limit', 1)
            memory_percent = (memory_usage / memory_limit) * 100.0
            
            return {
                'cpu_percent': round(cpu_percent, 2),
                'memory_usage_mb': round(memory_usage / (1024 ** 2), 2),
                'memory_percent': round(memory_percent, 2)
            }
            
        except Exception as e:
            logger.error(f"Error getting container stats: {e}")
            return None
    
    def _is_dangerous_command(self, command):
        """
        Basic command filtering for security.
        Block obviously dangerous commands.
        """
        dangerous_patterns = [
            'rm -rf /',
            'mkfs',
            'dd if=',
            'fork bomb',
            ':(){ :|:& };:',
        ]
        
        command_lower = command.lower()
        return any(pattern.lower() in command_lower for pattern in dangerous_patterns)
