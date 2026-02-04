from django.urls import path
from . import views

urlpatterns = [
    path('balance/', views.ether_balance, name='ether-balance'),
    path('transactions/', views.EtherTransactionListView.as_view(), name='ether-transactions'),
    path('clan/transactions/', views.ClanTransactionListView.as_view(), name='clan-transactions'),
    path('clan/wallet/', views.clan_wallet_status, name='clan-wallet'),
]
