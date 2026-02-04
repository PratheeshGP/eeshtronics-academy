"""
Mission and Exercise models - Core learning activities.
"""
from django.db import models
from apps.core.models import TimeStampedModel


class Mission(TimeStampedModel):
    """
    A mission is a specific learning task within a module.
    Example: "Build a Half Adder", "Design a Flip-Flop"
    """
    DIFFICULTY_CHOICES = [
        ('EASY', 'Easy'),
        ('MEDIUM', 'Medium'),
        ('HARD', 'Hard'),
        ('EXPERT', 'Expert'),
    ]
    
    ARTIFACT_TYPE_CHOICES = [
        ('CODE', 'Code Submission'),
        ('DIAGRAM', 'Circuit Diagram'),
        ('REPORT', 'Written Report'),
        ('VIDEO', 'Video Demo'),
        ('FILE', 'File Upload'),
    ]
    
    module = models.ForeignKey('modules.Module', on_delete=models.CASCADE, related_name='missions')
    
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='MEDIUM')
    order = models.IntegerField(default=0)
    
    # Instructions
    mission_brief = models.TextField(help_text="Detailed mission instructions")
    hints = models.JSONField(default=list, help_text="List of hints")
    
    # Validation
    required_artifact_type = models.CharField(max_length=20, choices=ARTIFACT_TYPE_CHOICES, default='CODE')
    validation_script = models.TextField(blank=True, help_text="Python script to validate submission")
    auto_validate = models.BooleanField(default=False)
    
    # Rewards
    xp_reward = models.IntegerField(default=100)
    ether_reward = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    
    # Estimated time
    estimated_minutes = models.IntegerField(default=30)
    
    # Lab association
    requires_lab = models.BooleanField(default=False)
    associated_lab = models.ForeignKey('labs.Lab', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['module', 'order']
        unique_together = ('module', 'slug')
    
    def __str__(self):
        return f"{self.module.title} - {self.title}"


class Exercise(TimeStampedModel):
    """
    Exercises are smaller tasks within a mission.
    """
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='exercises')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0)
    
    # Validation
    expected_output = models.TextField(blank=True)
    test_cases = models.JSONField(default=list)
    
    # Rewards
    xp_reward = models.IntegerField(default=25)
    
    class Meta:
        ordering = ['mission', 'order']
    
    def __str__(self):
        return f"{self.mission.title} - {self.title}"


class Artifact(TimeStampedModel):
    """
    User submissions for missions.
    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='artifacts')
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='artifacts')
    
    # Submission
    submission_type = models.CharField(max_length=20, choices=Mission.ARTIFACT_TYPE_CHOICES)
    content = models.TextField(blank=True, help_text="Text content or code")
    file = models.FileField(upload_to='artifacts/', null=True, blank=True)
    
    # Validation
    is_validated = models.BooleanField(default=False)
    validation_result = models.JSONField(default=dict, help_text="Validation output")
    score = models.IntegerField(default=0, help_text="Score out of 100")
    
    # Feedback
    feedback = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.mission.title} - {self.created_at.date()}"
