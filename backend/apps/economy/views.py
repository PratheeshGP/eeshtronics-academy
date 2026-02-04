from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import EtherTransaction, ClanTransaction
from .serializers import EtherTransactionSerializer, ClanTransactionSerializer


@api_view(['GET'])
def ether_balance(request):
    """
    Get user's current Ether balance.
    GET /api/ether/balance
    """
    return Response({
        'balance': float(request.user.ether_balance),
        'username': request.user.username,
        'level': request.user.level
    })


class EtherTransactionListView(generics.ListAPIView):
    """List user's Ether transaction history."""
    serializer_class = EtherTransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return EtherTransaction.objects.filter(user=self.request.user)


class ClanTransactionListView(generics.ListAPIView):
    """List clan's transaction history."""
    serializer_class = ClanTransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.clan:
            return ClanTransaction.objects.filter(clan=self.request.user.clan)
        return ClanTransaction.objects.none()


@api_view(['GET'])
def clan_wallet_status(request):
    """Get clan wallet information."""
    if not request.user.clan:
        return Response({'error': 'User not in a clan'}, status=400)
    
    return Response({
        'clan_name': request.user.clan.name,
        'clan_ether': float(request.user.clan.clan_ether),
        'member_count': request.user.clan.member_count
    })
