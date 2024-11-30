from django.utils import timezone
from rest_framework import serializers
from .models import Client, Project, User
from django.contrib.auth.models import User
from django.contrib.auth.models import User as AuthUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by', 'updated_at']

    def get_created_by(self, obj):
        if obj.created_by:
            return obj.created_by.username
        return None

class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    users = serializers.SlugRelatedField(slug_field='username', queryset=AuthUser.objects.all(), many=True)    
    client_name = serializers.CharField(source='client.client_name', read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'client_name', 'users', 'created_at', 'created_by', 'updated_at']
    
    def validate_users(self, value):
        if not value:
            raise serializers.ValidationError("At least one user must be assigned to the project.")
        return value

    def validate(self, data):
        project_name = data.get('project_name')
        client = data.get('client')
        if Project.objects.filter(project_name=project_name, client=client).exists():
            raise serializers.ValidationError("A project with this name and client already exists.")
        return data
    
class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project_name']

class ClientDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    projects = ProjectDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by', 'updated_at']

    def get_created_by(self, obj):
        return obj.created_by.username if obj.created_by else "Anonymous"    
    
    def update(self, instance, validated_data):
        instance.client_name = validated_data.get('client_name', instance.client_name)
        instance.updated_at = timezone.now()
        instance.save()
        return instance