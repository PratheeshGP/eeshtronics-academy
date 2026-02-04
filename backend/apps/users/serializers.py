"""
Serializers for User authentication and profile management.
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Clan


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile with progression stats."""
    clan_name = serializers.CharField(source='clan.name', read_only=True)
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'bio', 'avatar',
            'xp_points', 'level', 'ether_balance', 'streak_count',
            'clan', 'clan_name', 'created_at'
        )
        read_only_fields = ('xp_points', 'level', 'ether_balance', 'created_at')


class ClanSerializer(serializers.ModelSerializer):
    """Serializer for Clan information."""
    founder_username = serializers.CharField(source='founder.username', read_only=True)
    
    class Meta:
        model = Clan
        fields = (
            'id', 'name', 'description', 'founder', 'founder_username',
            'clan_ether', 'total_xp', 'member_count', 'is_public', 'max_members',
            'created_at'
        )
        read_only_fields = ('clan_ether', 'total_xp', 'member_count', 'created_at')
