"""
Lab models for sandbox environments.
"""
from django.db import models
from apps.core.models import TimeStampedModel


class Lab(TimeStampedModel):
    """
    Lab definition with Docker configuration.
    """
    LAB_TYPE_CHOICES = [
        ('VERILOG', 'Verilog HDL'),
        ('EMBEDDED', 'Embedded Systems'),
        ('LINUX', 'Linux Terminal'),
        ('PYTHON', 'Python Environment'),
        ('GENERAL', 'General Purpose'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    lab_type = models.CharField(max_length=20, choices=LAB_TYPE_CHOICES, default='GENERAL')
    
    # Docker configuration
    docker_image = models.CharField(
        max_length=200,
        help_text="Docker image name, e.g., 'ubuntu:22.04' or 'custom/verilog-env:latest'"
    )
    dockerfile_content = models.TextField(blank=True, help_text="Custom Dockerfile if needed")
    
    # Resource limits
    memory_limit = models.CharField(max_length=10, default='512m', help_text="e.g., '512m', '1g'")
    cpu_quota = models.IntegerField(default=50000, help_text="CPU quota in microseconds per 100ms")
    timeout_seconds = models.IntegerField(default=3600, help_text="Auto-terminate after this duration")
    
    # Network settings
    network_enabled = models.BooleanField(default=False, help_text="Enable network access (disabled for security)")
    
    # Initial setup
    startup_command = models.TextField(blank=True, help_text="Command to run on container start")
    environment_variables = models.JSONField(default=dict, help_text="Environment variables")
    
    # Validation
    validation_script = models.TextField(blank=True, help_text="Script to validate lab completion")
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class LabSession(TimeStampedModel):
    """
    Active or historical lab session for a user.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('STARTING', 'Starting'),
        ('RUNNING', 'Running'),
        ('STOPPED', 'Stopped'),
        ('ERROR', 'Error'),
        ('EXPIRED', 'Expired'),
    ]
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='lab_sessions')
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, related_name='sessions')
    mission = models.ForeignKey('missions.Mission', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Container info
    container_id = models.CharField(max_length=64, blank=True)
    container_name = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Session metadata
    started_at = models.DateTimeField(null=True, blank=True)
    stopped_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Usage tracking
    command_count = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.lab.name} ({self.status})"
    
    def is_active(self):
        return self.status == 'RUNNING'
