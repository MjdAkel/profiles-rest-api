from rest_framework import serializers
from profiles_api import models

from rest_framework import serializers

class HelloSerializer(serializers.Serializer):
    """Serializer for testing"""
    name = serializers.CharField(max_length=10)
    
# User Profile 
# Serializer for User Profile model
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'username', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)

    def validate_username(self, value):
        """Ensure username is unique"""
        if models.UserProfile.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        models=models.ProfileFeedItem
        Fields = ('id','user_profile','status_text','created_on')
        extra_kwargs={'user_profile':{'read_only':True}}
        