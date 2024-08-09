from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer
from .permission import IsSuperAdmin 
from django.contrib.auth.hashers import make_password

class UserAPIView(APIView):
    #permission_classes = [IsAuthenticated]
    
    
    def get(self, request, email=None, format=None):
        if email is None:
            # Liste des utilisateurs
            if not request.user.is_superuser:
                 return Response({"detail": "tu n'a pas la permission pour recuperer toute les users ."}, status=status.HTTP_403_FORBIDDEN)
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        else:
            # Détails d'un utilisateur
            try:
                user = User.objects.get(email=email)
                
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserSerializer(user)
            
            if request.user != user and not request.user.is_superuser:
                return Response({"detail": "tu n'a pas la permission pour recuperer se user ."}, status=status.HTTP_403_FORBIDDEN)
            return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            serializer.save(password=make_password(password))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, email, format=None):
        # Mettre à jour les informations d'un utilisateur
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "le User n'existe pas"}, status=status.HTTP_404_NOT_FOUND)

        
        if request.user != user and not request.user.is_superuser:
            return Response({"detail": "tu n'a pas la permission pour editer se user ."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, email, format=None):
        # Mise à jour partielle des informations d'un utilisateur
        return self.put(request, email, format)

    def delete(self, request, email, format=None):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "le User n'existe pas."}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(),IsSuperAdmin()]
        elif self.request.method in ['PUT', 'PATCH']:
            return [IsAuthenticated()]
        return []




