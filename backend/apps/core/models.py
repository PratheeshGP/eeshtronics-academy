"""
Base models and utilities shared across apps.
"""
from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract base model with created and updated timestamps.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    Abstract base model with soft delete capability.
    """
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True
