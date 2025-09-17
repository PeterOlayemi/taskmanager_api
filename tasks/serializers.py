from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Task

from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use")
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class TaskSerializer(serializers.ModelSerializer):
    owner_id = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='assignee', allow_null=True, required=False)
    assignee_username = serializers.ReadOnlyField(source='assignee.username')

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status',
            'owner_id', 'owner_username',
            'assignee_id', 'assignee_username',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner_id', 'owner_username', 'assignee_username', 'created_at', 'updated_at']
