"""
Custom User model with XP, Level, Ether, and Clan support.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    """
    Extended user model for EngineerLab platform.
    Tracks progression, currency, and clan membership.
    """
    email = models.EmailField(unique=True)
    
    # Progression tracking
    xp_points = models.IntegerField(default=0, help_text="Total experience points")
    level = models.IntegerField(default=1, help_text="User level calculated from XP")
    
    # Economy
    ether_balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=100.00,
        help_text="Platform currency balance"
    )
    
    # Engagement
    streak_count = models.IntegerField(default=0, help_text="Consecutive days active")
    last_active_date = models.DateField(null=True, blank=True)
    
    # Social
    clan = models.ForeignKey(
        'Clan', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='members'
    )
    
    # Profile
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    class Meta:
        ordering = ['-xp_points']
    
    def __str__(self):
        return self.username
    
    def calculate_level(self):
        """Calculate level based on XP points using exponential curve."""
        import math
        self.level = int(math.sqrt(self.xp_points / 100)) + 1
        return self.level
    
    def add_xp(self, amount):
        """Add XP and recalculate level."""
        self.xp_points += amount
        self.calculate_level()
        self.save()
    
    def add_ether(self, amount, description=""):
        """Add Ether to balance and log transaction."""
        from apps.economy.models import EtherTransaction
        self.ether_balance += amount
        self.save()
        
        EtherTransaction.objects.create(
            user=self,
            amount=amount,
            transaction_type='EARN',
            description=description
        )
    
    def spend_ether(self, amount, description=""):
        """Spend Ether if balance sufficient."""
        if self.ether_balance >= amount:
            self.ether_balance -= amount
            self.save()
            
            from apps.economy.models import EtherTransaction
            EtherTransaction.objects.create(
                user=self,
                amount=-amount,
                transaction_type='SPEND',
                description=description
            )
            return True
        return False


class Clan(TimeStampedModel):
    """
    User groups for collaborative learning and competition.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    founder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='founded_clans')
    
    # Pooled resources
    clan_ether = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Stats
    total_xp = models.IntegerField(default=0)
    member_count = models.IntegerField(default=0)
    
    # Settings
    is_public = models.BooleanField(default=True)
    max_members = models.IntegerField(default=50)
    
    class Meta:
        ordering = ['-total_xp']
    
    def __str__(self):
        return self.name
