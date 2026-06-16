"""
Progress tracking models for user learning journey.
"""
from django.db import models
from apps.core.models import TimeStampedModel


class MissionProgress(TimeStampedModel):
    """Track user progress on missions."""
    STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='mission_progress')
    mission = models.ForeignKey('missions.Mission', on_delete=models.CASCADE, related_name='user_progress')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOT_STARTED')
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    score = models.IntegerField(default=0, help_text="Score out of 100")
    
    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent_seconds = models.IntegerField(default=0)
    
    # Attempts
    attempt_count = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('user', 'mission')
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.mission.title} ({self.status})"
    
    def mark_complete(self, score=100):
        """Mark mission as completed and award rewards."""
        from django.utils import timezone
        
        self.status = 'COMPLETED'
        self.progress_percentage = 100.00
        self.score = score
        self.completed_at = timezone.now()
        self.save()
        
        # Award XP and Ether
        self.user.add_xp(self.mission.xp_reward)
        self.user.add_ether(
            float(self.mission.ether_reward),
            f"Completed mission: {self.mission.title}"
        )


class UserStreak(TimeStampedModel):
    """Track user daily activity streaks."""
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='streak')
    
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.current_streak} day streak"
    
    def update_streak(self):
        """Update streak based on today's activity."""
        from datetime import date
        
        today = date.today()
        
        if not self.last_activity_date:
            # First activity
            self.current_streak = 1
            self.longest_streak = 1
        elif self.last_activity_date == today:
            # Already active today
            return
        elif (today - self.last_activity_date).days == 1:
            # Consecutive day
            self.current_streak += 1
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
        else:
            # Streak broken
            self.current_streak = 1
        
        self.last_activity_date = today
        self.user.streak_count = self.current_streak
        self.user.save()
        self.save()


class Achievement(TimeStampedModel):
    """Platform achievements/badges."""
    CATEGORY_CHOICES = [
        ('MISSION', 'Mission Completion'),
        ('STREAK', 'Activity Streak'),
        ('SKILL', 'Skill Mastery'),
        ('SOCIAL', 'Social Contribution'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    # Requirements
    requirement_description = models.TextField()
    requirement_value = models.IntegerField(help_text="e.g., 10 missions, 7 day streak")
    
    # Rewards
    xp_reward = models.IntegerField(default=500)
    ether_reward = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    
    # Icon
    icon = models.ImageField(upload_to='achievements/', null=True, blank=True)
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return self.name


class UserAchievement(TimeStampedModel):
    """Track user-earned achievements."""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'achievement')
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"


class RequirementTracker(TimeStampedModel):
    """
    Model for tracking user-submitted files/requirements.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('IN_PROGRESS', 'Under Review'),
        ('COMPLETED', 'Completed'),
        ('REJECTED', 'Rejected'),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='requirements')
    title = models.CharField(max_length=200, help_text="What requirement/file is being uploaded")
    description = models.TextField(blank=True, help_text="Additional details/requirements description")
    file = models.FileField(upload_to='requirements/', help_text="Uploaded document or artifact")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    admin_notes = models.TextField(blank=True, help_text="Feedback or progress notes from administrator")
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.status})"
