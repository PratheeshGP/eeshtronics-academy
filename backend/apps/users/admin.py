from django.contrib import admin
from .models import User, Clan


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'level', 'xp_points', 'ether_balance', 'clan')
    list_filter = ('level', 'clan')
    search_fields = ('username', 'email')


@admin.register(Clan)
class ClanAdmin(admin.ModelAdmin):
    list_display = ('name', 'founder', 'member_count', 'total_xp', 'clan_ether')
    search_fields = ('name',)
