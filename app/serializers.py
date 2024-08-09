from rest_framework import serializers
from .models import Projet, Tache
from users.models import User
from datetime import timedelta


class ProjectSerializer(serializers.ModelSerializer):
    my_user_data = serializers.SerializerMethodField(read_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = Projet
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'email', 'my_user_data']

    def get_my_user_data(self, obj):
        return {
            "email": obj.manger.email,
            "nom": obj.manger.nom
        }

    def create(self, validated_data):
        email = validated_data.pop('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "User with this email does not exist."})
        
        project = Projet.objects.create(manger=user, **validated_data)
        return project
    
    # def validate(self, data):
    #     if data.get('end_date') is None:
    #         data['end_date'] = data['start_date'] + timedelta(days=30)
    #     return data
            

        
class Tasheserializer(serializers.ModelSerializer):
    my_Projec_data = serializers.SerializerMethodField(read_only=True)
    my_user_data =serializers.SerializerMethodField(read_only=True)
    
    projet = serializers.PrimaryKeyRelatedField(
        queryset=Projet.objects.all(), 
        write_only=True
    )
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        write_only=True
    )
    class Meta:
        model = Tache
        fields = ['id', 'titre', 'description', 'start_date', 'end_date', 'projet','my_Projec_data', 'assigned_to','my_user_data', 'status']
        
    def get_my_Projec_data(self,obj):
        return{
            "name":obj.projet.name,
            "start_date":obj.projet.start_date,
            "end_date":obj.projet.end_date
        }
        
    def get_my_user_data(self,obj):
        return {
            "email": obj.assigned_to.email,
            "nom": obj.assigned_to.nom
        }