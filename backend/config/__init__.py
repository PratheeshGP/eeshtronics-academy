"""
Django initialization for config package.
Loads Celery app for async task processing.
"""

from .celery import app as celery_app

__all__ = ('celery_app',)
