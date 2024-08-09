from django.shortcuts import render
from .models import Projet,Tache
from .serializers import ProjectSerializer, Tasheserializer
from rest_framework import generics,authentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permission import IsManager,IsProjectManager,IsTashAssigneeOrManager,IsTashProjetManager
from rest_framework import status
from rest_framework.exceptions import NotFound
    
class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Projet.objects.all()
    serializer_class = ProjectSerializer
    #permission_classes = [IsAuthenticated]
    
    # def get_permissions(self):
    #     if self.request.method == 'POST':
    #         self.permission_classes = [IsManager]
    #     return super().get_permissions()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProjectSerializer(queryset, many=True)
        #return super().list(request, *args, **kwargs)
        return Response(serializer.data)
    
    
    def perform_create(self, serializer):
        #name = serializer.validated_data.get('name')
        description = serializer.validated_data.get('description') or None
        if description is None :
            description = " Pour plus des information contacter le chef de projet"
        serializer.save(description=description)
        
        
        
class ProjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Projet.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticated, IsProjectManager]
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": "Le projet a été supprimé avec succès"}, status=status.HTTP_200_OK)
        except NotFound:
            return Response({"detail": "Le projet n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
        
        
class TashListCreateView(generics.ListCreateAPIView):
    queryset = Tache.objects.all()
    serializer_class = Tasheserializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated, IsManager]
        return super().get_permissions()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = Tasheserializer(queryset, many=True)
        #return super().list(request, *args, **kwargs)
        return Response(serializer.data)

class TashRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tache.objects.all()
    serializer_class = Tasheserializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [IsTashAssigneeOrManager]
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsTashProjetManager]
        return super().get_permissions()
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": "La tache a été supprimé avec succès"}, status=status.HTTP_200_OK)
        except NotFound:
            return Response({"detail": "Le tache n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
# Create your views here.
