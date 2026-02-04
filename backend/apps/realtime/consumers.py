"""
WebSocket consumer for real-time lab terminal interaction.
"""
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from apps.sandbox.docker_executor import DockerSandboxExecutor

logger = logging.getLogger(__name__)


class LabTerminalConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for interactive terminal sessions in labs.
    Handles bidirectional communication between user and Docker container.
    """
    
    async def connect(self):
        """Handle WebSocket connection."""
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.user = self.scope['user']
        
        # Verify session belongs to user
        session = await self.get_lab_session()
        if not session or session.user != self.user:
            await self.close()
            return
        
        self.container_id = session.container_id
        self.session = session
        
        await self.accept()
        
        # Send welcome message
        await self.send(text_data=json.dumps({
            'type': 'connection',
            'message': f'Connected to lab: {session.lab.name}',
            'container_id': self.container_id
        }))
        
        logger.info(f"WebSocket connected for session {self.session_id}")
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        logger.info(f"WebSocket disconnected for session {self.session_id}")
    
    async def receive(self, text_data):
        """
        Receive command from WebSocket and execute in container.
        """
        try:
            data = json.loads(text_data)
            command = data.get('command', '')
            
            if not command:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'No command provided'
                }))
                return
            
            # Execute command in container
            result = await self.execute_command(command)
            
            # Send result back to client
            await self.send(text_data=json.dumps({
                'type': 'output',
                'command': command,
                'output': result.get('output', ''),
                'error': result.get('error', ''),
                'exit_code': result.get('exit_code', 0)
            }))
            
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON'
            }))
        except Exception as e:
            logger.error(f"Error in WebSocket receive: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': str(e)
            }))
    
    @database_sync_to_async
    def get_lab_session(self):
        """Get lab session from database."""
        from apps.labs.models import LabSession
        try:
            return LabSession.objects.get(id=self.session_id)
        except LabSession.DoesNotExist:
            return None
    
    @database_sync_to_async
    def execute_command(self, command):
        """Execute command in Docker container."""
        executor = DockerSandboxExecutor()
        return executor.execute_command(self.container_id, command, self.session)
