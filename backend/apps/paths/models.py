"""
Learning Path models - Top level of learning hierarchy.
"""
from django.db import models
from apps.core.models import TimeStampedModel


class Path(TimeStampedModel):
    """
    A learning path represents a complete learning journey.
    Example: "Digital Electronics Fundamentals", "VLSI Design"
    """
    DIFFICULTY_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
        ('EXPERT', 'Expert'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='BEGINNER')
    
    # Progression
    estimated_hours = models.IntegerField(help_text="Estimated completion time in hours")
    order = models.IntegerField(default=0, help_text="Display order")
    
    # Rewards
    completion_xp = models.IntegerField(default=1000)
    completion_ether = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    
    # Media
    thumbnail = models.ImageField(upload_to='paths/', null=True, blank=True)
    
    # Metadata
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order', 'title']
        verbose_name_plural = 'Paths'
    
    def __str__(self):
        return self.title
    
    def get_module_count(self):
        return self.modules.count()
    
    def get_total_missions(self):
        from apps.missions.models import Mission
        return Mission.objects.filter(module__path=self).count()


class PathEnrollment(TimeStampedModel):
    """Track user enrollment in learning paths."""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='path_enrollments')
    path = models.ForeignKey(Path, on_delete=models.CASCADE, related_name='enrollments')
    
    # Progress
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'path')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.path.title}"
