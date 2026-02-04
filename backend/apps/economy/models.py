"""
Economy models for Ether currency system.
"""
from django.db import models
from apps.core.models import TimeStampedModel


class EtherTransaction(TimeStampedModel):
    """
    Log all Ether currency transactions.
    """
    TRANSACTION_TYPE_CHOICES = [
        ('EARN', 'Earned'),
        ('SPEND', 'Spent'),
        ('TRANSFER', 'Transferred'),
        ('REWARD', 'Reward'),
        ('REFUND', 'Refund'),
    ]
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='ether_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    description = models.TextField()
    
    # Optional related objects
    mission = models.ForeignKey('missions.Mission', on_delete=models.SET_NULL, null=True, blank=True)
    module = models.ForeignKey('modules.Module', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Balance after transaction
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        sign = '+' if self.amount >= 0 else ''
        return f"{self.user.username}: {sign}{self.amount} Ether - {self.description}"


class ClanWallet(TimeStampedModel):
    """
    Shared wallet for clans.
    """
    clan = models.OneToOneField('users.Clan', on_delete=models.CASCADE, related_name='wallet')
    total_contributed = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.clan.name} Wallet"


class ClanTransaction(TimeStampedModel):
    """
    Log clan wallet transactions.
    """
    TRANSACTION_TYPE_CHOICES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdrawal'),
        ('REWARD', 'Clan Reward'),
    ]
    
    clan = models.ForeignKey('users.Clan', on_delete=models.CASCADE, related_name='clan_transactions')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='clan_contributions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    description = models.TextField()
    
    # Balance after transaction
    clan_balance_after = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.clan.name} - {self.user.username}: {self.amount} Ether"
