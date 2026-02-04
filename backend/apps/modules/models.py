"""
Module models - Second level of learning hierarchy.
Modules group related missions within a path.
"""
from django.db import models
from apps.core.models import TimeStampedModel


class Module(TimeStampedModel):
    """
    A module is a collection of related missions within a learning path.
    Example: "Boolean Algebra", "Sequential Circuits"
    """
    path = models.ForeignKey('paths.Path', on_delete=models.CASCADE, related_name='modules')
    
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField()
    order = models.IntegerField(default=0)
    
    # Prerequisites
    prerequisite_modules = models.ManyToManyField('self', symmetrical=False, blank=True)
    
    # Economy
    ether_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        help_text="Ether required to unlock this module"
    )
    
    # Rewards
    completion_xp = models.IntegerField(default=300)
    completion_ether = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    
    # Metadata
    learning_objectives = models.JSONField(default=list, help_text="List of learning objectives")
    estimated_hours = models.IntegerField(default=5)
    is_locked_by_default = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['path', 'order']
        unique_together = ('path', 'slug')
    
    def __str__(self):
        return f"{self.path.title} - {self.title}"
    
    def get_mission_count(self):
        return self.missions.count()


class ModuleUnlock(TimeStampedModel):
    """Track which modules users have unlocked."""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='unlocked_modules')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='unlocks')
    
    # Completion tracking
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'module')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.module.title}"
