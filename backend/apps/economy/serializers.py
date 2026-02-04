from rest_framework import serializers
from .models import EtherTransaction, ClanWallet, ClanTransaction


class EtherTransactionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = EtherTransaction
        fields = (
            'id', 'user', 'username', 'amount', 'transaction_type',
            'description', 'mission', 'module', 'balance_after', 'created_at'
        )
        read_only_fields = ('balance_after',)


class ClanWalletSerializer(serializers.ModelSerializer):
    clan_name = serializers.CharField(source='clan.name', read_only=True)
    current_balance = serializers.DecimalField(source='clan.clan_ether', max_digits=12, decimal_places=2, read_only=True)
    
    class Meta:
        model = ClanWallet
        fields = ('id', 'clan', 'clan_name', 'current_balance', 'total_contributed')


class ClanTransactionSerializer(serializers.ModelSerializer):
    clan_name = serializers.CharField(source='clan.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ClanTransaction
        fields = (
            'id', 'clan', 'clan_name', 'user', 'username', 'amount',
            'transaction_type', 'description', 'clan_balance_after', 'created_at'
        )
