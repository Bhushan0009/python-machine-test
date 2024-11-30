from django.shortcuts import render
from rest_framework import generics,permissions, exceptions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Client, Project ,User
from .serializers import ClientSerializer, ProjectSerializer, ClientDetailSerializer
from rest_framework.views import APIView


class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.prefetch_related('projects')
    serializer_class = ClientDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(users=user) | Project.objects.filter(created_by=user)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise exceptions.NotAuthenticated("You need to be logged in to create a project.")
        serializer.save(created_by=self.request.user)
    
class ProjectDetailView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk, format=None):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    
    def delete(self, request, pk, format=None):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        # Delete the project
        project.delete()
        return Response({"detail": "Project deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


    
class ClientUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save() 